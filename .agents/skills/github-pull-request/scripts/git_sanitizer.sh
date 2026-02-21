#!/bin/bash

# Git Data Sanitization Script for GitHub PR Skill (Bash version)
#
# This script provides utilities to sanitize untrusted data from git sources
# before using them in LLM prompts and PR templates.
#
# Usage:
#   source git_sanitizer.sh
#   sanitize_commit_message "$raw_msg"
#   extract_safe_diff_stats "main" "feature-branch"

set -euo pipefail

# Configuration
MAX_COMMIT_LENGTH=300
MAX_DIFF_LINES=5000
VERBOSE="${VERBOSE:-0}"

# Color codes for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Injection marker patterns to detect
declare -a INJECTION_MARKERS=(
    '\[SYSTEM[:\]'
    '\[IGNORE\]'
    '\[BYPASS'
    '\[OVERRIDE'
    '<!--.*SYSTEM'
    '<!--.*IGNORE'
    '<!--.*BYPASS'
    '{{.*SYSTEM'
    '{%.*SYSTEM'
)

# Suspicious keywords in commit messages
declare -a SUSPICIOUS_KEYWORDS=(
    'ALWAYS BYPASS'
    'NEVER REVIEW'
    'AUTO-APPROVE'
    'SKIP VALIDATION'
    'SKIP CHECKS'
    'DISABLE SECURITY'
    'OVERRIDE RULES'
    'IGNORE POLICY'
    'FORCE MERGE'
    'IMMEDIATE ACTION'
    'URGENT - BYPASS'
    'CRITICAL - SKIP'
)

#######################################
# Log message with optional verbosity
#######################################
log_verbose() {
    if [[ $VERBOSE -eq 1 ]]; then
        echo "[VERBOSE] $*" >&2
    fi
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*" >&2
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*" >&2
}

#######################################
# Sanitize a commit message
#######################################
sanitize_commit_message() {
    local msg="$1"
    local max_length="${2:-$MAX_COMMIT_LENGTH}"
    
    local sanitized="$msg"
    local red_flags=()
    
    log_verbose "Sanitizing commit message (length: ${#msg})"
    
    # Check for injection patterns
    for pattern in "${INJECTION_MARKERS[@]}"; do
        if echo "$sanitized" | grep -qiE "$pattern"; then
            log_warning "Detected injection marker: $pattern"
            red_flags+=("injection_marker_detected")
            sanitized=$(echo "$sanitized" | sed -E "s/$pattern/[REDACTED]/gi")
        fi
    done
    
    # Check for suspicious keywords
    for keyword in "${SUSPICIOUS_KEYWORDS[@]}"; do
        if echo "$sanitized" | grep -qi "$(echo "$keyword" | sed 's/ /.*/')"; then
            log_warning "Detected suspicious keyword: $keyword"
            red_flags+=("suspicious_keyword")
        fi
    done
    
    # Remove excessive whitespace
    sanitized=$(echo "$sanitized" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    sanitized=$(echo "$sanitized" | sed '/^$/d')  # Remove blank lines
    
    # Truncate if too long
    if [[ ${#sanitized} -gt $max_length ]]; then
        log_verbose "Truncating message from ${#sanitized} to $max_length chars"
        sanitized="${sanitized:0:$max_length}...[TRUNCATED]"
        red_flags+=("content_truncated")
    fi
    
    # Output results as JSON
    local is_suspicious="false"
    [[ ${#red_flags[@]} -gt 0 ]] && is_suspicious="true"
    
    cat <<EOF
{
  "content": $(echo "$sanitized" | jq -Rs .),
  "is_suspicious": $is_suspicious,
  "red_flags": $(printf '%s\n' "${red_flags[@]}" | jq -R . | jq -s .),
  "original_length": ${#msg},
  "sanitized_length": ${#sanitized}
}
EOF
}

#######################################
# Extract safe diff statistics
#######################################
extract_safe_diff_stats() {
    local base_branch="$1"
    local head_branch="$2"
    
    log_verbose "Extracting diff stats from $base_branch...$head_branch"
    
    # Get diff stats
    local diff_output
    if ! diff_output=$(git diff "$base_branch...$head_branch" --stat 2>&1); then
        log_error "Failed to get diff stats"
        echo '{"error": "Failed to get diff stats", "files_changed": 0}'
        return 1
    fi
    
    local files_changed=0
    local total_insertions=0
    local total_deletions=0
    local files_json="[]"
    
    # Parse diff output
    local file_entries="[]"
    while IFS= read -r line; do
        # Skip summary line
        if [[ "$line" == *"changed"* ]]; then
            continue
        fi
        
        # Parse: "path | changes"
        if [[ "$line" =~ \|  ]]; then
            local filepath=$(echo "$line" | cut -d'|' -f1 | xargs)
            local changes=$(echo "$line" | cut -d'|' -f2 | xargs)
            
            # Safety check: skip if path has injection markers
            if echo "$filepath" | grep -qE '\[|<!--|{{|{%'; then
                log_warning "Skipping suspicious filepath: $filepath"
                continue
            fi
            
            ((files_changed++))
            
            # Extract insertion/deletion counts
            local insertions=$(echo "$changes" | grep -oE '[0-9]+' | head -1 || echo 0)
            local deletions=$(echo "$changes" | grep -oE '[0-9]+' | tail -1 || echo 0)
            
            total_insertions=$((total_insertions + insertions))
            total_deletions=$((total_deletions + deletions))
            
            # Add to JSON array
            file_entries=$(echo "$file_entries" | jq --arg path "$filepath" --arg changes "$changes" \
                '. += [{"path": $path, "changes": $changes}]')
        fi
    done <<< "$diff_output"
    
    cat <<EOF
{
  "files_changed": $files_changed,
  "insertions": $total_insertions,
  "deletions": $total_deletions,
  "files": $file_entries
}
EOF
}

#######################################
# Get sanitized commit summary
#######################################
get_commit_summary() {
    local base_branch="$1"
    local head_branch="$2"
    local max_commits="${3:-10}"
    
    log_verbose "Getting commit summary from $base_branch...$head_branch"
    
    local commit_count=0
    local commits_json="[]"
    local all_red_flags="[]"
    
    while IFS= read -r line; do
        [[ $commit_count -ge $max_commits ]] && break
        
        # Parse: "hash message"
        local hash=$(echo "$line" | cut -d' ' -f1)
        local message=$(echo "$line" | cut -d' ' -f2-)
        
        # Sanitize the message
        local sanitized_result
        sanitized_result=$(sanitize_commit_message "$message")
        
        local sanitized_msg=$(echo "$sanitized_result" | jq -r '.content')
        local flags=$(echo "$sanitized_result" | jq '.red_flags')
        
        commits_json=$(echo "$commits_json" | jq --arg hash "$hash" --arg msg "$sanitized_msg" \
            '. += [{"hash": $hash, "message": $msg}]')
        
        all_red_flags=$(echo "$all_red_flags" | jq ". += $flags")
        
        ((commit_count++))
    done < <(git log "$base_branch...$head_branch" --oneline --no-decorate 2>/dev/null || true)
    
    cat <<EOF
{
  "commits": $commits_json,
  "red_flags": $(echo "$all_red_flags" | jq -s 'unique'),
  "commit_count": $commit_count
}
EOF
}

#######################################
# Detect red flags in text
#######################################
detect_red_flags() {
    local text="$1"
    
    log_verbose "Scanning text for red flags"
    
    local flags_json="[]"
    
    # Check injection patterns
    for pattern in "${INJECTION_MARKERS[@]}"; do
        if echo "$text" | grep -qiE "$pattern"; then
            flags_json=$(echo "$flags_json" | jq '. += ["injection_marker"]')
        fi
    done
    
    # Check suspicious keywords
    for keyword in "${SUSPICIOUS_KEYWORDS[@]}"; do
        if echo "$text" | grep -qi "$(echo "$keyword" | sed 's/ /.*/')"; then
            flags_json=$(echo "$flags_json" | jq '. += ["suspicious_keyword"]')
        fi
    done
    
    # Check for excessive all-caps (5+ consecutive uppercase letters)
    if echo "$text" | grep -qE '[A-Z]{5,}'; then
        flags_json=$(echo "$flags_json" | jq '. += ["excessive_all_caps"]')
    fi
    
    # Check for excessive newlines
    local newline_count
    newline_count=$(echo "$text" | grep -c '^' || echo 0)
    if [[ $newline_count -gt 20 ]]; then
        flags_json=$(echo "$flags_json" | jq '. += ["excessive_newlines"]')
    fi
    
    echo "$flags_json" | jq -s 'unique | flatten'
}

#######################################
# Format safety report
#######################################
format_safety_report() {
    local commit_msg="$1"
    local diff_stats="$2"
    
    local sanitized_msg_result
    sanitized_msg_result=$(sanitize_commit_message "$commit_msg")
    
    local red_flags
    red_flags=$(echo "$sanitized_msg_result" | jq -r '.red_flags | join(", ")')
    local is_suspicious
    is_suspicious=$(echo "$sanitized_msg_result" | jq -r '.is_suspicious')
    
    echo "═══════════════════════════════════════════════════════════════════"
    echo "SECURITY ANALYSIS REPORT"
    echo "═══════════════════════════════════════════════════════════════════"
    echo ""
    
    if [[ "$is_suspicious" == "true" ]]; then
        echo -e "${RED}⚠️  RED FLAGS DETECTED:${NC}"
        echo "$red_flags" | tr ',' '\n' | sed 's/^ */  - /g'
        echo ""
    else
        echo -e "${GREEN}✅ No red flags detected${NC}"
        echo ""
    fi
    
    if [[ -n "$diff_stats" ]]; then
        local files_changed
        files_changed=$(echo "$diff_stats" | jq -r '.files_changed')
        local insertions
        insertions=$(echo "$diff_stats" | jq -r '.insertions')
        local deletions
        deletions=$(echo "$diff_stats" | jq -r '.deletions')
        
        echo "📊 CHANGES:"
        echo "   Files changed: $files_changed"
        echo "   Insertions: +$insertions"
        echo "   Deletions: -$deletions"
        echo ""
    fi
    
    echo "═══════════════════════════════════════════════════════════════════"
    echo "RECOMMENDATION:"
    
    if [[ "$is_suspicious" == "true" ]]; then
        echo -e "${RED}⚠️  REVIEW CAREFULLY - Potential injection attempt detected.${NC}"
        echo "Do not approve without manual verification."
    else
        echo -e "${GREEN}✅ Appears safe to proceed with PR creation.${NC}"
    fi
    
    echo "═══════════════════════════════════════════════════════════════════"
}

#######################################
# Main workflow example
#######################################
run_security_check() {
    local base_branch="${1:-main}"
    local head_branch="${2:-HEAD}"
    
    log_info "Starting security check for $base_branch...$head_branch"
    
    # Get latest commit message
    local commit_msg
    commit_msg=$(git log -1 --format=%B "$head_branch" 2>/dev/null || echo "")
    
    log_verbose "Commit message: $commit_msg"
    
    # Get diff stats
    local diff_stats
    diff_stats=$(extract_safe_diff_stats "$base_branch" "$head_branch")
    
    log_verbose "Diff stats: $diff_stats"
    
    # Format report
    format_safety_report "$commit_msg" "$diff_stats"
}

#######################################
# Export functions for sourcing
#######################################
export -f sanitize_commit_message
export -f extract_safe_diff_stats
export -f get_commit_summary
export -f detect_red_flags
export -f format_safety_report
export -f run_security_check

# If script is run directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [[ $# -eq 0 ]]; then
        echo "Usage: $0 [base_branch] [head_branch]"
        echo ""
        echo "Examples:"
        echo "  $0 main feature-branch"
        echo "  VERBOSE=1 $0 main"
        exit 1
    fi
    
    run_security_check "$@"
fi
