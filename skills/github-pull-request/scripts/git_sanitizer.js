#!/usr/bin/env node

/**
 * Git Data Sanitization Module for GitHub PR Skill (JavaScript/Node.js)
 *
 * This module provides utilities to sanitize untrusted data from git sources
 * before using them in LLM prompts and PR templates.
 *
 * Usage:
 *   const { GitDataSanitizer } = require('./git_sanitizer.js');
 *   const sanitizer = new GitDataSanitizer();
 *   const result = sanitizer.sanitizeCommitMessage(rawMsg);
 */

const { execSync, spawnSync } = require('child_process');
const path = require('path');

/**
 * Git Data Sanitizer Class
 */
class GitDataSanitizer {
    constructor(config = {}) {
        this.maxCommitLength = config.maxCommitLength || 300;
        this.maxDiffLines = config.maxDiffLines || 5000;
        this.verbose = config.verbose || false;

        // Injection patterns
        this.injectionPatterns = {
            systemInstruction: /\[SYSTEM[:\]].+/gi,
            ignoreDirective: /\[IGNORE\].+/gi,
            overrideDirective: /\[(BYPASS|OVERRIDE|SECURITY)[:\]].+/gi,
            htmlCommentInjection: /<!--\s*(SYSTEM|IGNORE|BYPASS).+?-->/gi,
            yamlInjection: /^\s*(SYSTEM|IGNORE|BYPASS):.+$/gim,
            templateLiteral: /\{\{.+?(SYSTEM|IGNORE|BYPASS).+?\}\}/gi,
            jinjaInjection: /\{%.*?(SYSTEM|IGNORE|BYPASS).*?%\}/gi,
        };

        // Suspicious keywords
        this.suspiciousKeywords = [
            'ALWAYS BYPASS', 'NEVER REVIEW', 'AUTO-APPROVE',
            'SKIP VALIDATION', 'SKIP CHECKS', 'DISABLE SECURITY',
            'OVERRIDE RULES', 'IGNORE POLICY', 'FORCE MERGE',
            'IMMEDIATE ACTION', 'URGENT - BYPASS', 'CRITICAL - SKIP',
        ];
    }

    /**
     * Log with optional verbosity
     */
    log(level, message) {
        if (this.verbose || level === 'error' || level === 'warning') {
            const timestamp = new Date().toISOString();
            const prefix = {
                verbose: '[VERBOSE]',
                info: '[INFO]',
                warning: '⚠️  [WARNING]',
                error: '❌ [ERROR]',
                success: '✅ [SUCCESS]',
            }[level] || '[LOG]';

            console.error(`${prefix} ${message}`);
        }
    }

    /**
     * Sanitize a commit message
     * @param {string} msg - Raw commit message
     * @returns {Object} Sanitization result
     */
    sanitizeCommitMessage(msg) {
        const originalLength = msg.length;
        const redFlags = [];
        let sanitized = msg;

        this.log('verbose', `Sanitizing commit message (length: ${originalLength})`);

        // Check for injection patterns
        for (const [patternName, pattern] of Object.entries(this.injectionPatterns)) {
            if (pattern.test(sanitized)) {
                this.log('warning', `Detected injection pattern: ${patternName}`);
                redFlags.push(patternName);
                sanitized = sanitized.replace(pattern, '[REDACTED]');
            }
        }

        // Check for suspicious keywords
        for (const keyword of this.suspiciousKeywords) {
            const keywordPattern = new RegExp(keyword.split(' ').join('.*'), 'i');
            if (keywordPattern.test(sanitized)) {
                this.log('warning', `Detected suspicious keyword: ${keyword}`);
                redFlags.push(`suspicious_keyword_${keyword.replace(/\s+/g, '_')}`);
            }
        }

        // Remove excessive whitespace
        sanitized = sanitized
            .replace(/\n\n+/g, '\n')
            .replace(/ {2,}/g, ' ')
            .trim();

        // Truncate if too long
        if (sanitized.length > this.maxCommitLength) {
            this.log('verbose', `Truncating from ${sanitized.length} to ${this.maxCommitLength} chars`);
            sanitized = sanitized.slice(0, this.maxCommitLength) + '...[TRUNCATED]';
            redFlags.push('content_truncated');
        }

        return {
            content: sanitized,
            isSuspicious: redFlags.length > 0,
            redFlags,
            originalLength,
            sanitizedLength: sanitized.length,
        };
    }

    /**
     * Extract safe diff statistics
     * @param {string} baseBranch - Base branch name
     * @param {string} headBranch - Head branch name
     * @returns {Object} Safe statistics
     */
    extractSafeDiffStats(baseBranch, headBranch) {
        try {
            this.log('verbose', `Extracting diff stats from ${baseBranch}...${headBranch}`);

            const result = spawnSync('git', [
                'diff',
                `${baseBranch}...${headBranch}`,
                '--stat'
            ], {
                encoding: 'utf-8',
                timeout: 5000
            });

            if (result.status !== 0) {
                this.log('error', 'Failed to get diff stats');
                return { error: 'Failed to get diff stats', files_changed: 0 };
            }

            return this.parseDiffStats(result.stdout);
        } catch (error) {
            this.log('error', `Unexpected error: ${error.message}`);
            return { error: error.message, files_changed: 0 };
        }
    }

    /**
     * Parse git diff --stat output safely
     * @private
     */
    parseDiffStats(output) {
        const stats = {
            files_changed: 0,
            insertions: 0,
            deletions: 0,
            files: [],
        };

        const lines = output.trim().split('\n');

        for (const line of lines) {
            // Skip summary lines
            if (!line.includes('|') || line.includes('changed')) {
                continue;
            }

            try {
                const parts = line.split('|');
                if (parts.length !== 2) continue;

                const filepath = parts[0].trim();
                const changes = parts[1].trim();

                // Safety: skip if filepath has injection markers
                if (/[\[\<\{%]/.test(filepath)) {
                    this.log('warning', `Skipping suspicious filepath: ${filepath}`);
                    continue;
                }

                stats.files.push({
                    path: filepath,
                    changes,
                });
                stats.files_changed += 1;

                // Extract numbers safely
                const numbers = changes.match(/\d+/g) || [];
                if (numbers.length >= 1) stats.insertions += parseInt(numbers[0], 10);
                if (numbers.length >= 2) stats.deletions += parseInt(numbers[1], 10);
            } catch (error) {
                this.log('warning', `Error parsing line: ${line}`);
                continue;
            }
        }

        return stats;
    }

    /**
     * Get sanitized commit summary
     * @param {string} baseBranch - Base branch
     * @param {string} headBranch - Head branch
     * @param {number} maxCommits - Maximum commits to include
     * @returns {Object} Commit summary with red flags
     */
    getCommitSummary(baseBranch, headBranch, maxCommits = 10) {
        try {
            this.log('verbose', `Getting commit summary from ${baseBranch}...${headBranch}`);

            const result = spawnSync('git', [
                'log',
                `${baseBranch}...${headBranch}`,
                '--oneline',
                '--no-decorate',
                `-${maxCommits}`
            ], {
                encoding: 'utf-8'
            });

            if (result.status !== 0) {
                return { commits: [], red_flags: [], commit_count: 0 };
            }

            const commits = [];
            const allRedFlags = new Set();

            const lines = result.stdout.trim().split('\n').filter(line => line.length > 0);

            for (const line of lines) {
                const [hash, ...msgParts] = line.split(' ');
                const message = msgParts.join(' ');

                const sanitized = this.sanitizeCommitMessage(message);
                commits.push({
                    hash,
                    message: sanitized.content,
                });

                sanitized.redFlags.forEach(flag => allRedFlags.add(flag));
            }

            return {
                commits,
                red_flags: Array.from(allRedFlags),
                commit_count: commits.length,
            };
        } catch (error) {
            this.log('error', `Error retrieving commits: ${error.message}`);
            return { commits: [], red_flags: ['error_retrieving_commits'], commit_count: 0 };
        }
    }

    /**
     * Comprehensive red flag detection
     * @param {string} text - Text to analyze
     * @returns {Array} List of red flags
     */
    detectAllRedFlags(text) {
        const redFlags = new Set();

        // Check injection patterns
        for (const pattern of Object.values(this.injectionPatterns)) {
            if (pattern.test(text)) {
                redFlags.add('injection_pattern_detected');
            }
        }

        // Check suspicious keywords
        for (const keyword of this.suspiciousKeywords) {
            const keywordPattern = new RegExp(keyword.split(' ').join('.*'), 'i');
            if (keywordPattern.test(text)) {
                redFlags.add('suspicious_keyword');
            }
        }

        // Check for unusual formatting
        const allCapsMatches = text.match(/[A-Z]{5,}/g) || [];
        if (allCapsMatches.length > 3) {
            redFlags.add('excessive_all_caps');
        }

        const newlineCount = (text.match(/\n/g) || []).length;
        if (newlineCount > 20) {
            redFlags.add('excessive_newlines');
        }

        return Array.from(redFlags);
    }

    /**
     * Format a safety report for user review
     * @param {Object} results - Sanitization results
     * @returns {string} Formatted report
     */
    formatSafetyReport(results) {
        let report = '═'.repeat(70) + '\n';
        report += 'SECURITY ANALYSIS REPORT\n';
        report += '═'.repeat(70) + '\n\n';

        if (results.red_flags && results.red_flags.length > 0) {
            report += '⚠️  RED FLAGS DETECTED:\n';
            for (const flag of results.red_flags) {
                report += `   - ${flag}\n`;
            }
            report += '\n';
        } else {
            report += '✅ No red flags detected\n\n';
        }

        if (results.files_changed) {
            report += '📊 CHANGES:\n';
            report += `   Files changed: ${results.files_changed}\n`;
            report += `   Insertions: +${results.insertions}\n`;
            report += `   Deletions: -${results.deletions}\n\n`;
        }

        if (results.suspicious_commits && results.suspicious_commits.length > 0) {
            report += '🔍 SUSPICIOUS COMMITS:\n';
            for (const commit of results.suspicious_commits) {
                report += `   - ${commit}\n`;
            }
            report += '\n';
        }

        report += '═'.repeat(70) + '\n';
        report += 'RECOMMENDATION:\n';

        if (results.red_flags && results.red_flags.length > 0) {
            report += '⚠️  REVIEW CAREFULLY - Potential injection attempt detected.\n';
            report += 'Do not approve without manual verification.\n';
        } else {
            report += '✅ Appears safe to proceed with PR creation.\n';
        }

        report += '═'.repeat(70) + '\n';

        return report;
    }
}

/**
 * Main workflow example
 */
function runSecurityCheck(baseBranch = 'main', headBranch = 'HEAD') {
    const sanitizer = new GitDataSanitizer({ verbose: true });

    console.error('\n' + '='.repeat(70));
    console.error('RUNNING SECURITY CHECK');
    console.error('='.repeat(70) + '\n');

    try {
        // Get latest commit message
        const commitResult = spawnSync('git', [
            'log',
            '-1',
            '--format=%B',
            headBranch
        ], { encoding: 'utf-8' });

        const commitMsg = commitResult.stdout || '';

        // Get diff stats
        const diffStats = sanitizer.extractSafeDiffStats(baseBranch, headBranch);

        // Get commit summary
        const commitSummary = sanitizer.getCommitSummary(baseBranch, headBranch);

        // Combine results
        const results = {
            ...diffStats,
            red_flags: commitSummary.red_flags,
            commits: commitSummary.commits,
            suspicious_commits: commitSummary.commits
                .filter(c => sanitizer.detectAllRedFlags(c.message).length > 0)
                .map(c => c.message)
        };

        // Format and display report
        console.log(sanitizer.formatSafetyReport(results));

    } catch (error) {
        console.error(`Error during security check: ${error.message}`);
        process.exit(1);
    }
}

// Export for use as module
module.exports = { GitDataSanitizer };

// If run directly
if (require.main === module) {
    const args = process.argv.slice(2);
    const baseBranch = args[0] || 'main';
    const headBranch = args[1] || 'HEAD';
    runSecurityCheck(baseBranch, headBranch);
}
