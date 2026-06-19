/* Progress tracking (TW-4). Runs only for signed-in users; calls /api/progress.
   Hooks (all optional, present per page):
   - #lesson-progress[data-course][data-lesson]  : mark-complete control on a lesson
   - [data-slug][data-course] list items + #course-progress : ticks + % on a course page
   - #account-progress                            : progress summary on /account        */
(function () {
  function key(course, lesson) { return course + '::' + lesson; }

  // Escape values from the API before they go into innerHTML. The /api/progress
  // course/lesson fields are free-text the user can set (via POST), so they must
  // be treated as untrusted — same discipline as account.astro / admin/index.astro.
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  fetch('/.auth/me', { headers: { accept: 'application/json' } })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (me) {
      var p = me && me.clientPrincipal;
      if (!p) return null; // anonymous — leave the page as-is
      return fetch('/api/progress', { headers: { accept: 'application/json' } })
        .then(function (r) { return r.ok ? r.json() : { items: [] }; })
        .then(function (data) {
          var items = (data && data.items) || [];
          var completed = new Set(
            items.filter(function (i) { return i.type === 'progress' && i.status === 'completed'; })
                 .map(function (i) { return key(i.course, i.lesson); })
          );
          initLesson(completed);
          initCourse(completed);
          initAccount(items);
        });
    })
    .catch(function () {});

  function initLesson(completed) {
    var el = document.getElementById('lesson-progress');
    if (!el) return;
    var course = el.getAttribute('data-course');
    var lesson = el.getAttribute('data-lesson');
    var done = completed.has(key(course, lesson));
    el.hidden = false;
    render();
    function render() {
      el.innerHTML = done
        ? '<span class="done-badge">✓ Completed</span> <button class="btn secondary" type="button" id="mc-btn">Mark not complete</button>'
        : '<button class="btn" type="button" id="mc-btn">Mark lesson complete</button>';
      document.getElementById('mc-btn').addEventListener('click', function () {
        var btn = this; btn.disabled = true;
        fetch('/api/progress', {
          method: 'POST', headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ course: course, lesson: lesson, status: done ? 'in-progress' : 'completed' }),
        }).then(function (r) { if (r.ok) { done = !done; render(); } else { btn.disabled = false; } })
          .catch(function () { btn.disabled = false; });
      });
    }
  }

  function initCourse(completed) {
    var items = document.querySelectorAll('li[data-slug][data-course]');
    if (!items.length) return;
    var total = 0, doneN = 0, firstIncomplete = null;
    items.forEach(function (li) {
      total++;
      var slug = li.getAttribute('data-slug');
      if (completed.has(key(li.getAttribute('data-course'), slug))) {
        li.classList.add('lesson-done'); doneN++;
      } else if (!firstIncomplete) {
        firstIncomplete = slug;
      }
    });
    var bar = document.getElementById('course-progress');
    if (bar && total) {
      bar.hidden = false;
      bar.textContent = doneN + ' / ' + total + ' lessons complete (' + Math.round((doneN / total) * 100) + '%)';
    }
    var resume = document.getElementById('course-resume');
    if (resume && total) {
      if (firstIncomplete) {
        resume.setAttribute('href', '/topics/' + firstIncomplete + '/');
        resume.hidden = false;
      } else {
        resume.textContent = 'Course complete ✓';
        resume.removeAttribute('href');
        resume.hidden = false;
      }
    }
  }

  function initAccount(items) {
    var box = document.getElementById('account-progress');
    if (!box) return;
    var done = items.filter(function (i) { return i.type === 'progress' && i.status === 'completed'; });
    var byCourse = {};
    done.forEach(function (i) { (byCourse[i.course] = byCourse[i.course] || []).push(i); });
    var courses = Object.keys(byCourse);
    var html = '<h2>Your progress</h2>';
    if (!courses.length) {
      html += '<p class="theme">No lessons completed yet — open a course and mark a lesson complete.</p>';
    } else {
      html += '<ul class="topic-list">' + courses.map(function (c) {
        return '<li>' + esc(c) + ' — <strong>' + byCourse[c].length + '</strong> lesson' + (byCourse[c].length === 1 ? '' : 's') + ' complete</li>';
      }).join('') + '</ul>';
    }
    box.innerHTML = html;
  }
})();
