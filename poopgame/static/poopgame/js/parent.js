// parent.js

document.addEventListener('DOMContentLoaded', () => {
    const list = document.querySelector('.chore-list ul');
    const pointCountEl = document.getElementById('point-count');
  
    list.addEventListener('click', e => {
      if (!e.target.classList.contains('btn-award')) return;
  
      const li = e.target.closest('li');
      const choreId = li.getAttribute('data-id');
      const btn = e.target;
  
      btn.disabled = true;
      btn.textContent = '付与中…';
  
      fetch("", {
        method: 'POST',
        headers: {
          'X-CSRFToken': document.querySelector('input[name=csrfmiddlewaretoken]').value,
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          action: 'award_chore',
          chore_id: choreId
        })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          pointCountEl.textContent = data.new_points;
          btn.textContent = '付与済み';
        } else {
          btn.textContent = 'エラー';
        }
      })
      .catch(() => {
        btn.textContent = 'エラー';
      });
    });
  });
  