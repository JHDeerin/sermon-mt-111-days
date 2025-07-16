const r = require("./docs/diff_highlight");

test('correctly marks diff with contraction in input', () => {
    expect(getDiffOutputHtml(
        "You are the salt of the earth. But if salt has lost its taste, how shall its saltiness be restored? It is no longer good for anything except to be thrown out and trampled under people's feet. You are the light of the world. A city set on a hill can be hidden x",
        `"You are the salt of the earth, but if salt has lost its taste, how shall its saltiness be restored? It is no longer good for anything except to be thrown out and trampled under people's feet.\n\"You are the light of the world. A city set on a hill cannot be hidden.`
    )).toBe(`You are the salt of the earth. But if salt has lost its taste, how shall its saltiness be restored? It is no longer good for anything except to be thrown out and trampled under people's feet. You are the light of the world. A city set on a hill<span class="deleted-placeholder" title="Deleted: cannot"> </span> <span class="added">can</span> be hidden <span class="added">x</span>`)
});

test('correctly ignores iOS safari quotes', () => {
    expect(getDiffOutputHtml(
        `“You are the salt of the earth”`,
        `"You are the salt of the earth"`
    )).toBe(`“You are the salt of the earth”`)
});

test('correctly ignores iOS safari apostrophes', () => {
    expect(getDiffOutputHtml(
        `Trampled under people’s feet. ‘Quote’`,
        `Trampled under people's feet. 'Quote'`
    )).toBe(`Trampled under people’s feet. ‘Quote’`)
});

test('correctly ignores punctuation for correctness', () => {
    expect(getDiffOutputHtml(
        `trampled under peoples feet.`,
        `trampled under people's feet`
    )).toBe(`trampled under peoples feet.`)
});

test('punctuation normalization bug - words incorrectly combined', () => {
    // Test case for GitHub issue: "Fix normalization of punctuation incorrectly combining words"
    // The bug occurs when normalizeWordSegment removes punctuation without adding spaces

    // Example from the issue: "them.For" should normalize to match "them for"
    // Due to the bug, this returns the original text unchanged because of the mismatch
    expect(getDiffOutputHtml("them.For", "them for MISSING")).toBe(`them.For<span class="deleted-placeholder" title="Deleted: missing"> </span>`);

    // Additional test cases that demonstrate the bug
    expect(getDiffOutputHtml("word.another added", "word another")).toBe(`word.another <span class="added">added</span>`);
    expect(getDiffOutputHtml("hello,world added", "hello world")).toBe(`hello,world <span class="added">added</span>`);
    expect(getDiffOutputHtml("test:case added", "test case")).toBe(`test:case <span class="added">added</span>`);
    expect(getDiffOutputHtml("one;two.three added", "one two three")).toBe(`one;two.three <span class="added">added</span>`);
});
