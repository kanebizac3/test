// parent.js

document.addEventListener('DOMContentLoaded', () => {
    const list = document.querySelector('.chore-list ul');
    const pointCountEl = document.getElementById('point-count');
  
    list.addEventListener('click', e => {
      const li = e.target.closest('li');
      const choreId = li?.getAttribute('data-id');
      const csrf  = document.querySelector('input[name=csrfmiddlewaretoken]').value;
  
      // ポイント付与
      if (e.target.classList.contains('btn-award')) {
        const btn = e.target;
        btn.disabled = true;
        btn.textContent = '付与中…';
  
        fetch("", {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrf,
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
        .catch(() => btn.textContent = 'エラー');
      }
  
      // お手伝い削除
      if (e.target.classList.contains('btn-delete')) {
        const btn = e.target;
        btn.disabled = true;
        btn.textContent = '削除中…';
  
        fetch("", {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrf,
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            action: 'delete_chore',
            chore_id: choreId
          })
        })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            li.remove();  // DOMから削除
          } else {
            btn.textContent = '失敗';
          }
        })
        .catch(() => btn.textContent = 'エラー');
      }
    });
  });
  