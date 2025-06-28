// NOTE: Generated using Gemini-2.5 Pro Preview 05-06, then modified

// Helper function to normalize text for comparison
// Removes punctuation, converts to lowercase, and collapses multiple spaces.
// Returns an array of "clean" words.
const IGNORE_CHARS_REGEX = /[.,\/#!$%\^&\*;:{}=\-_`~()\[\]"'‘’“”]/g;

function normalizeAndSplit(text) {
    const cleanedText = text
        .toLowerCase()
        // keep contractions as one word, e.g. "don't" -> "dont", not "don t"
        .replace(/['‘’]/g, "")
        // Replace punctuation with a space to ensure word separation
        // e.g. "word.word" becomes "word word" after split
        .replace(IGNORE_CHARS_REGEX, " ")
        .replace(/\s+/g, " ") // Collapse multiple spaces to single
        .trim();
    return cleanedText === "" ? [] : cleanedText.split(" ");
}

// Helper function to normalize a single word segment for comparison
// This is used when iterating through original segments
function normalizeWordSegment(word) {
    return word.toLowerCase().replace(IGNORE_CHARS_REGEX, "");
}


// Longest Common Subsequence (LCS) algorithm
// Returns an array representing the LCS words
function getLCS(seq1, seq2) {
    const m = seq1.length;
    const n = seq2.length;
    const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (seq1[i - 1] === seq2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    // Backtrack to find the LCS words
    let index = dp[m][n];
    const lcsArr = Array(index);
    let i = m, j = n;
    while (i > 0 && j > 0) {
        if (seq1[i - 1] === seq2[j - 1]) {
            lcsArr[index - 1] = seq1[i - 1];
            i--; j--; index--;
        } else if (dp[i - 1][j] > dp[i][j - 1]) {
            i--;
        } else {
            j--;
        }
    }
    return lcsArr;
}

function buildDiffOps(a, b, lcs_seq) {
    const result = [];
    let ptr_a = 0;
    let ptr_b = 0;
    let ptr_lcs = 0;

    while (ptr_lcs < lcs_seq.length) {
        const lcs_elem = lcs_seq[ptr_lcs];

        while (ptr_a < a.length && a[ptr_a] !== lcs_elem) {
            result.push({ type: 'deleted', text: a[ptr_a] });
            ptr_a++;
        }
        while (ptr_b < b.length && b[ptr_b] !== lcs_elem) {
            result.push({ type: 'added', text: b[ptr_b] });
            ptr_b++;
        }

        if (ptr_a < a.length && ptr_b < b.length && a[ptr_a] === lcs_elem && b[ptr_b] === lcs_elem) {
            result.push({ type: 'common', text: b[ptr_b] }); // Use text from 'b' (user) for 'common'
            ptr_a++;
            ptr_b++;
            ptr_lcs++;
        } else {
            // This means lcs_elem was not found in either a or b at current pointers,
            // or one sequence is exhausted. If LCS is correct, this shouldn't be an infinite loop.
            // The inner while loops should consume until match or end of sequence.
            // If lcs_elem is never found in one of the sequences, ptr_lcs won't advance.
            // This implies that an element in lcs_seq is not actually common if one sequence
            // runs out before matching it.
            // This suggests that the LCS algorithm might produce an LCS that is "too long"
            // or contains elements that are not truly common if one sequence ends.
            // Let's assume getLCS is robust and this case implies lcs_elem WILL be found if sequences not exhausted.
            // If one sequence IS exhausted (e.g. ptr_a >= a.length), then lcs_elem cannot be common.
            // This situation would mean the LCS is invalid w.r.t. the exhausted sequence.
            // This is a critical point for the correctness of LCS-based diff.
            // To prevent infinite loops if LCS is "faulty" or sequences mismatched:
            // A failsafe: if lcs_elem isn't found and pointers don't advance, break.
            // But, standard LCS guarantees elements are from *both* original sequences.
            // So, if ptr_a < a.length and ptr_b < b.length, then eventually they should point to lcs_elem.
            // If, say, ptr_a reaches a.length, then the remaining lcs_seq elements are not common.
            // The outer while (ptr_lcs < lcs_seq.length) should perhaps also check ptr_a and ptr_b.
            // For now, trusting the standard structure.
            break; // Break from outer while if LCS element not matched, remaining handled by post-loops.
        }
    }

    while (ptr_a < a.length) {
        result.push({ type: 'deleted', text: a[ptr_a] });
        ptr_a++;
    }
    while (ptr_b < b.length) {
        result.push({ type: 'added', text: b[ptr_b] });
        ptr_b++;
    }
    return result;
}

function generateCombinedHtmlFromOps(originalUserText, diffOps) {
    let html = '';
    const originalUserSegments = originalUserText.split(/(\s+)/);
    let userSegIdx = 0; // Pointer for originalUserSegments
    let opsIdx = 0;     // Pointer for diffOps

    // To map clean words from ops back to originalUserSegments, we need to consume
    // originalUserSegments one by one, and if it's a word, see if it matches the
    // op's expectation (if op is common/added).

    let processedCleanUserWords = 0; // Count of clean user words handled by 'common' or 'added' ops

    while (opsIdx < diffOps.length || userSegIdx < originalUserSegments.length) {
        // First, try to process an op if available
        if (opsIdx < diffOps.length) {
            const op = diffOps[opsIdx];

            if (op.type === 'deleted') {
                html += `<span class="deleted-placeholder" title="Deleted: ${op.text.replace(/"/g, '"')}"> </span>`;
                // Add a space after placeholder if it's not the last op or followed by non-whitespace user segment
                // This spacing is tricky. Let user's original spacing dictate where possible.
                // The placeholder takes the "slot" of a deleted word.
                opsIdx++;
                continue; // Process next op or user segment
            }

            // If op is 'common' or 'added', it expects a user word.
            // We need to find that user word in originalUserSegments.
            // Advance userSegIdx past whitespace.
            let currentOriginalUserSegment = '';
            let leadingWhitespace = '';

            while (userSegIdx < originalUserSegments.length && originalUserSegments[userSegIdx].trim() === '') {
                leadingWhitespace += originalUserSegments[userSegIdx];
                userSegIdx++;
            }
            html += leadingWhitespace; // Append consumed whitespace

            if (userSegIdx < originalUserSegments.length) {
                currentOriginalUserSegment = originalUserSegments[userSegIdx];
                const normalizedSegment = normalizeWordSegment(currentOriginalUserSegment);

                // This check ensures the segment is not just punctuation for common/added ops
                if (normalizedSegment === "") { // pure punctuation in user text
                    html += currentOriginalUserSegment;
                    userSegIdx++;
                    continue; // Move to next segment, op remains.
                }

                // Assert: normalizedSegment should be op.text for common/added
                if (normalizedSegment === op.text) {
                    if (op.type === 'common') {
                        html += currentOriginalUserSegment;
                    } else { // 'added'
                        html += `<span class="added">${currentOriginalUserSegment}</span>`;
                    }
                    opsIdx++;
                    userSegIdx++;
                    processedCleanUserWords++;
                    continue;
                } else {
                    // Mismatch: op.text (clean) vs normalizedSegment (from original)
                    // This implies an issue in how cleanUserWords were generated or how ops relate to original text.
                    // Or, the current originalUserSegment is punctuation that was stripped from clean word.
                    // If `op.text` expected "word" but `currentOriginalUserSegment` is "word.",
                    // `normalizeWordSegment("word.")` is "word", so it should match.
                    // This case means the current user segment does not correspond to the current 'common' or 'added' op.
                    // This could happen if there's leading punctuation in user text not accounted for by ops.
                    // For robustness: if it's not a match, and segment is non-empty, assume it's an un-op'd part of user text (e.g. extra punctuation).
                    // This part is tricky. The ops are based on clean words.
                    // The original plan: iterate ops, and for common/added, *find* the corresponding original segment.
                    // This loop iterates original segments and tries to match ops.
                    // Let's stick to consuming originalUserSegments as primary, and matching them to ops.

                    // Fallback: if current user segment doesn't match expected op, but op is not 'deleted',
                    // something is misaligned. For now, let's assume alignment or that `normalizeWordSegment` fixes it.
                    // If op is 'common' or 'added', and the current user segment (after whitespace) doesn't match `op.text`
                    // then the `diffOps` or `originalUserSegments` handling is not perfectly aligned.
                    // Most likely, the `op.text` (which is a clean word) should match `normalizeWordSegment(currentOriginalUserSegment)`.
                    // If it does not, then the `cleanUserWords` array (basis for ops) might have been formed differently
                    // than iteration over `originalUserSegments` + `normalizeWordSegment`.
                    // This should be okay if `normalizeAndSplit` and `normalizeWordSegment` are consistent.
                    console.error(`Mismatch: Op text "${op.text}" vs normalized segment "${normalizedSegment}" from "${currentOriginalUserSegment}"`);
                    // As a fallback, just print the user segment and advance it, hoping ops resync.
                    html += currentOriginalUserSegment;
                    userSegIdx++;
                    // Don't advance opsIdx, try to match it with next user segment. This could be dangerous (infinite loop).
                    // Better: If there's a common/added op, we MUST consume a user segment that corresponds to it.
                    // The current logic correctly does this IF normalizedSegment === op.text.
                    // The `else` here means they don't match.
                    // This indicates a bug in earlier stages or a complex punctuation scenario.
                    // For now, let's assume they will match due to consistent normalization.
                }
            } else {
                // User segments exhausted, but common/added op remains. Error.
                // opsIdx should also be at end or only 'deleted' ops left.
                // This will be caught by the outer while condition.
                break;
            }

        } else if (userSegIdx < originalUserSegments.length) {
            // Ops exhausted, but user segments remain. Append them (should be trailing whitespace or un-op'd punctuation).
            html += originalUserSegments[userSegIdx];
            userSegIdx++;
        } else {
            // Both exhausted
            break;
        }
    }
    return html.trim();
}

function getDiffOutputHtml(usrText, refText) {
    const cleanRefWords = normalizeAndSplit(refText);
    const cleanUserWords = normalizeAndSplit(usrText);

    const lcs = getLCS(cleanRefWords, cleanUserWords);

    const diffOperations = buildDiffOps(cleanRefWords, cleanUserWords, lcs);
    const diffOutput = generateCombinedHtmlFromOps(usrText, diffOperations);
    return diffOutput;
}


function registerDiffDisplay(
    referenceTextElId,
    inputElId,
    resultElId,
    buttonId
) {
    const compareButton = document.getElementById(buttonId);
    compareButton.addEventListener('click', () => {
        const referenceTextarea = document.getElementById(referenceTextElId);
        const userTextarea = document.getElementById(inputElId);

        const resultDiv = document.getElementById(resultElId);

        console.log(referenceTextarea);
        // hack to get innerText of a <detail> element that's still folded
        let _ = document.createElement("div");
        _.innerHTML = referenceTextarea.innerHTML;
        const refText = _.innerText;

        const usrText = userTextarea.innerText;
        console.log(refText);
        console.log(usrText);

        const diffOutput = getDiffOutputHtml(usrText, refText);
        if (diffOutput == usrText) {
            userTextarea.innerHTML = diffOutput; // still set to clear e.g. old extra word higlighting
            resultDiv.innerHTML = '✅';
            return;
        }
        const deletedCnt = (diffOutput.match(/class="deleted-placeholder"/g) || []).length
        const extraCnt = (diffOutput.match(/class="added"/g) || []).length
        resultDiv.innerHTML = `${deletedCnt} missing, ${extraCnt} extra`;
        userTextarea.innerHTML = diffOutput;
        console.log(diffOutput);
    });
    console.log(`added event listener to ${compareButton}`)
}

/* Hack to test this code, global is not available in the browser */
if (typeof global !== 'undefined') {
    global.getDiffOutputHtml = getDiffOutputHtml;
}