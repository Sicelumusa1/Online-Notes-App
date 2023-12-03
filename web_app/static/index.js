
document.addEventListener('DOMContentLoaded', function () {
const addNote = document.getElementById('add_note')
const allNotesBtn = document.getElementById('all_notes')
const notesListItem = document.querySelectorAll('.list-group-item')
let notePad = document.querySelector('.note')
const edit = document.getElementById('edit')
const done = document.getElementById('done')
const delEditBtn = document.querySelectorAll('.delEditBtn')

// Navigate around My Notes page

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
  
  // Event listeners
  addNote.addEventListener('click', (e) => toggleNotePadAndNotes(e, true));
  allNotesBtn.addEventListener('click', (e) => toggleNotePadAndNotes(e, false));
  edit.addEventListener('click', (e) =>toggleDelEditBtn(e, true));
  done.addEventListener('click', (e) => toggleDelEditBtn(e, false));
});
