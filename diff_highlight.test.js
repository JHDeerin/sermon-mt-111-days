const r = require("./docs/diff_highlight");

test('correctly marks diff with contraction in input', () => {
    expect(getDiffOutputHtml(
        "You are the salt of the earth. But if salt has lost its taste, how shall its saltiness be restored? It is no longer good for anything except to be thrown out and trampled under people's feet. You are the light of the world. A city set on a hill can be hidden x",
        `"You are the salt of the earth, but if salt has lost its taste, how shall its saltiness be restored? It is no longer good for anything except to be thrown out and trampled under people's feet.\n\"You are the light of the world. A city set on a hill cannot be hidden.`
    )).toBe(`You are the salt of the earth. But if salt has lost its taste, how shall its saltiness be restored? It is no longer good for anything except to be thrown out and trampled under people's feet. You are the light of the world. A city set on a hill<span class="deleted-placeholder" title="Deleted: cannot"> </span> <span class="added">can</span> be hidden <span class="added">x</span>`)
});