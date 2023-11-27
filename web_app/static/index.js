
const addNote = document.getElementById('add_note')
const allNotesBtn = document.getElementById('all_notes')
const notesListItem = document.querySelectorAll('.list-group-item')
const notePad = document.querySelector('.note')
const edit = document.getElementById('edit')
const done = document.getElementById('done')
const delEditBtn = document.querySelectorAll('.delEditBtn')
const delNote = document.getElementById('delete_Note')


// Navigate around My Notes page
// document.addEventListener('DOMContentLoaded', function () {
  function toggleNotePadAndNotes(e, showNotePad) {
    e.preventDefault();
  
    notesListItem.forEach(item => {
      item.style.display = showNotePad ? 'none' : 'block';
    });
  
    addNote.style.display = showNotePad ? 'none' : 'block';
    notePad.style.display = showNotePad ? 'block' : 'none';
    allNotesBtn.style.display = showNotePad ? 'block' : 'none';
  }
  
  
  function toggleDelEditBtn(e, showButtons) {
    e.preventDefault();
  
    delEditBtn.forEach(item => {
      item.style.display = showButtons ? 'flex' : 'none';
    });
  
    edit.style.display = showButtons ? 'none' : 'block';
    done.style.display = showButtons ? 'block' : 'none';
  }

  // delete a note
  function deleteNote(noteId) {
    fetch('/delete_note', {
      method: 'POST',
      body: JSON.stringify({noteId: noteId}),
    }).then((res) => {
      console.log('Server response:', res)
      return res.json();
    }).then((data) => {
      console.log('Server data:', data);
      window.location.href = '';
    }).catch((error) => {
      console.error('Error:', error)
    })
  }

  
  // Event listeners
  addNote.addEventListener('click', (e) => toggleNotePadAndNotes(e, true));
  allNotesBtn.addEventListener('click', (e) => toggleNotePadAndNotes(e, false));
  edit.addEventListener('click', (e) =>toggleDelEditBtn(e, true));
  done.addEventListener('click', (e) => toggleDelEditBtn(e, false));
  delNote.addEventListener('click', () => deleteNote( '{{ note.id }}' ))
// });
