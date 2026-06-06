async function saveNote() {

    const note = document.getElementById("noteInput").value;

    if (note.trim() === "") {
        alert("Please enter a note.");
        return;
    }

    await fetch("/add_note", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            note: note
        })
    });

    document.getElementById("noteInput").value = "";

    loadNotes();
}

async function loadNotes() {

    const response = await fetch("/get_notes");
    const notes = await response.json();

    const container = document.getElementById("notesContainer");

    container.innerHTML = "";

    notes.forEach(note => {

        const div = document.createElement("div");

        div.className = "note";

        div.innerHTML = `
            <p>${note.content}</p>
        `;

        container.appendChild(div);
    });
}

window.onload = loadNotes;