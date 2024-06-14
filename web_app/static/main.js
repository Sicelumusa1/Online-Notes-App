
document.addEventListener('DOMContentLoaded', function () {

  const addNote = document.getElementById('add_note')
  const allNotesBtn = document.getElementById('all_notes')
  const notesListItem = document.querySelectorAll('.list-group-item')
  const noteContainer = document.querySelector('.note')
  const edit = document.getElementById('edit')
  const done = document.getElementById('done')
  const delEditBtn = document.querySelectorAll('.delEditBtn')

// Navigate around My Notes page

function toggleNotePadAndNotes(showNotePad) {
  
  notesListItem.forEach(item => {
    item.style.display = showNotePad ? 'none' : 'block';
  });

  addNote.style.display = showNotePad ? 'none' : 'block';
  noteContainer.style.display = showNotePad ? 'block' : 'none';
  allNotesBtn.style.display = showNotePad ? 'block' : 'none';
}


function toggleDelEditBtn(showButtons) {
  
  delEditBtn.forEach(item => {
    item.style.display = showButtons ? 'flex' : 'none';
  });

  edit.style.display = showButtons ? 'none' : 'block';
  done.style.display = showButtons ? 'block' : 'none';
}


// Event listeners
addNote.addEventListener('click', () => toggleNotePadAndNotes(true));
allNotesBtn.addEventListener('click', () => toggleNotePadAndNotes(false));
edit.addEventListener('click', () => toggleDelEditBtn(true));
done.addEventListener('click',  () => toggleDelEditBtn(false));


const alert = document.querySelectorAll('.alert')

  alert.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity 0.5s';
      alert.style.opacity = 0;
    }, 5000)
  });

  // Notes searching functionality
document.getElementById('search-button').addEventListener('click', function () {
  const searchTermElement = document.getElementById('search-input');
  const notes = document.querySelectorAll('.list-group-item');

  if (searchTermElement) {
    const searchTerm = searchTermElement.value.toLowerCase();
    notes.forEach(function (note) {
      const noteKeywordsElement = note.querySelector('.data');
      if (noteKeywordsElement) {
        const noteKeywords = noteKeywordsElement.textContent.toLowerCase();
        if (noteKeywords.includes(searchTerm)) {
          note.style.display = 'block';
        } else {
          note.style.display = 'none';
        }
      }
      
    });

    // Clear seach field
    searchTermElement.value = '';

    // Toggle the visibility of the 'All_Notes' button
    allNotesBtn.style.display = 'block';
  }
  
});
});