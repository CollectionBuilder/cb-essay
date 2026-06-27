---
layout: print-hub
title: Print & PDF
permalink: /print/
sitemap: false
search_exclude: true
---

<div class="print-hub">
{% assign essay_count = site.essay | size %}

  <div class="print-hub-header">
    <h1>Print &amp; PDF</h1>
    <p>{% if essay_count == 1 %}Print or save this essay as a PDF.{% else %}Print individual essays or build a custom PDF book from the full collection.{% endif %}</p>
  </div>

  <!-- Featured essay (shown via JS when ?essay= URL param is present) -->
  <div class="print-hub-featured" id="print-featured" aria-live="polite">
    <h2 class="featured-label">Print This Essay</h2>
    <p class="featured-title" id="featured-title"></p>
    <a class="featured-print-btn" id="featured-print-btn" href="#" target="_blank" rel="noopener">
      <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" viewBox="0 0 16 16" aria-hidden="true">
        <path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/>
        <path d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/>
      </svg>
      Print Essay
    </a>
  </div>

  <!-- Book builder -->
  {% assign sorted_essays = site.essay | sort: "order" %}
  {% assign show_book = site.data.theme.print.show-book | default: true %}
  {% if show_book != false %}
  <div class="print-hub-section">
    <h2>{% if essay_count == 1 %}Print Options{% else %}Build the Book{% endif %}</h2>
    <div class="book-builder">
      {% if essay_count > 1 %}
      <div class="book-filter-row">
        <input class="book-filter" id="chapter-filter" type="search" placeholder="Filter chapters…" aria-label="Filter chapter list" autocomplete="off">
        <div class="book-filter-actions">
          <button class="book-action-btn" id="select-all-btn" aria-label="Select all chapters">All</button>
          <span class="book-action-sep" aria-hidden="true">·</span>
          <button class="book-action-btn" id="deselect-all-btn" aria-label="Deselect all chapters">None</button>
          <button class="book-action-btn" id="select-filtered-btn" aria-label="Select all filtered chapters" hidden>Filtered</button>
        </div>
      </div>
      {% endif %}
      <ul class="book-checklist" id="book-checklist" {% if essay_count == 1 %}hidden{% endif %} aria-label="Chapters to include">
        {% for essay in sorted_essays %}{% assign url_key = essay.url | split: "/" | last | remove: ".html" %}
        <li>
          <input type="checkbox" id="book-{{ essay.slug }}" value="{{ url_key }}" data-url-key="{{ url_key }}" checked>
          <label for="book-{{ essay.slug }}">{{ essay.title }}</label>
        </li>
        {% endfor %}
      </ul>
      <div class="book-options">
        <div class="book-opt">
          <span class="book-opt-label">Format</span>
          <div class="format-hub-btns" role="group" aria-label="Page format">
            <button class="format-hub-btn" data-format="letter" aria-pressed="false">Letter</button>
            <button class="format-hub-btn" data-format="a4" aria-pressed="false">A4</button>
            <button class="format-hub-btn" data-format="69" aria-pressed="false">6×9″</button>
          </div>
        </div>
        <div class="book-opt">
          <span class="book-opt-label">Layout</span>
          <div class="layout-hub-btns" role="group" aria-label="Layout mode">
            <button class="layout-hub-btn" data-layout="digital" aria-pressed="false">Digital PDF</button>
            <button class="layout-hub-btn" data-layout="book" aria-pressed="false">Print Book</button>
          </div>
        </div>
        {% if site.data.theme.featured-image %}
        <div class="book-opt">
          <span class="book-opt-label">Cover</span>
          <label class="book-checkbox-label">
            <input type="checkbox" id="cover-image-toggle" checked>
            <span>Include cover image</span>
          </label>
        </div>
        {% endif %}
      </div>
      <button class="book-generate-btn" id="book-generate-btn">{% if essay_count == 1 %}Generate PDF{% else %}Generate Book PDF{% endif %}</button>
    </div>
  </div>
  {% endif %}

  <!-- Individual essays -->
  {% assign show_individual = site.data.theme.print.show-individual | default: true %}
  {% if show_individual != false and essay_count > 1 %}
  <div class="print-hub-section">
    <h2>Essays</h2>
    <div class="tributary-cards">
      {% for essay in sorted_essays %}{% assign url_key = essay.url | split: "/" | last | remove: ".html" %}
      <div class="tributary-card">
        <p class="card-title">{{ essay.title }}</p>
        <a class="card-link" href="{{ '/print/book/' | relative_url }}?essays={{ url_key }}&autoprint=1" target="_blank" aria-label="Print {{ essay.title | escape }}, opens in new tab">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" viewBox="0 0 16 16" aria-hidden="true">
            <path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/>
            <path d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/>
          </svg>
          Print Essay
        </a>
      </div>
      {% endfor %}
    </div>
  </div>
  {% endif %}

</div>

<script>
(function() {
  // ——— Essay metadata map (URL key → title) built from Liquid ———
  // essay.url gives the canonical URL (e.g. /essay/04-chapter-2-the-carpet-bag.html).
  // Splitting on "/" and stripping ".html" matches what section-nav extracts from
  // window.location.pathname — safe even when filenames contain dots.
  var essayTitles = {
    {% assign sorted_essays = site.essay | sort: "order" %}{% for essay in sorted_essays %}{% assign url_key = essay.url | split: "/" | last | remove: ".html" %}"{{ url_key }}": "{{ essay.title | escape }}"{% unless forloop.last %},{% endunless %}{% endfor %}
  };

  // ——— Persistent user preferences ———
  var formatMode = localStorage.getItem('print-format') || 'letter';
  var layoutMode = localStorage.getItem('print-layout') || 'digital';

  // ——— URL param: ?essay=url-key ———
  var params = new URLSearchParams(window.location.search);
  var featuredUrlKey = params.get('essay');

  if (featuredUrlKey && essayTitles[featuredUrlKey]) {
    var block = document.getElementById('print-featured');
    var titleEl = document.getElementById('featured-title');
    var btn = document.getElementById('featured-print-btn');

    titleEl.textContent = essayTitles[featuredUrlKey];
    btn.href = '{{ "/print/book/" | relative_url }}' + '?essays=' + featuredUrlKey + '&format=' + formatMode + '&autoprint=1';
    block.style.display = 'block';

    // Pre-check only this essay in the book builder
    document.querySelectorAll('#book-checklist input[type="checkbox"]').forEach(function(cb) {
      cb.checked = (cb.dataset.urlKey === featuredUrlKey);
    });
  }

  // ——— Format toggle ———
  document.querySelectorAll('.format-hub-btn').forEach(function(btn) {
    var isActive = btn.dataset.format === formatMode;
    btn.classList.toggle('active', isActive);
    btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    btn.addEventListener('click', function() {
      formatMode = this.dataset.format;
      localStorage.setItem('print-format', formatMode);
      document.querySelectorAll('.format-hub-btn').forEach(function(b) {
        var active = b.dataset.format === formatMode;
        b.classList.toggle('active', active);
        b.setAttribute('aria-pressed', active ? 'true' : 'false');
      });
    });
    btn.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') this.click();
    });
  });

  // ——— Layout toggle ———
  document.querySelectorAll('.layout-hub-btn').forEach(function(btn) {
    var isActive = btn.dataset.layout === layoutMode;
    btn.classList.toggle('active', isActive);
    btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    btn.addEventListener('click', function() {
      layoutMode = this.dataset.layout;
      localStorage.setItem('print-layout', layoutMode);
      document.querySelectorAll('.layout-hub-btn').forEach(function(b) {
        var active = b.dataset.layout === layoutMode;
        b.classList.toggle('active', active);
        b.setAttribute('aria-pressed', active ? 'true' : 'false');
      });
    });
    // Buttons activate on Enter natively, but be explicit for reliability
    btn.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') this.click();
    });
  });

  // ——— Cover image toggle ———
  var coverToggle = document.getElementById('cover-image-toggle');
  if (coverToggle) {
    // Restore localStorage preference (overrides theme.yml default)
    var storedCover = localStorage.getItem('print-cover-image');
    if (storedCover !== null) coverToggle.checked = (storedCover === 'true');
    coverToggle.addEventListener('change', function() {
      localStorage.setItem('print-cover-image', this.checked);
    });
    // Checkboxes toggle on Space by default; add Enter support for consistency
    coverToggle.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        this.checked = !this.checked;
        this.dispatchEvent(new Event('change'));
      }
    });
  }

  // ——— Book builder ———
  var generateBtn = document.getElementById('book-generate-btn');
  if (generateBtn) {
    generateBtn.addEventListener('click', function() {
      var checked = Array.from(
        document.querySelectorAll('#book-checklist input[type="checkbox"]:checked')
      ).map(function(cb) { return cb.value; });

      if (checked.length === 0) {
        alert('Select at least one essay to include.');
        return;
      }

      var url = '{{ "/print/book/" | relative_url }}' + '?essays=' + checked.join(',');
      url += '&format=' + formatMode;
      if (coverToggle && coverToggle.checked) url += '&cover=1';
      if (layoutMode === 'book') url += '&layout=book';
      url += '&autoprint=1';
      window.open(url, '_blank');
    });
  }

  // ——— Chapter filter ———
  var filterInput = document.getElementById('chapter-filter');
  var selectFilteredBtn = document.getElementById('select-filtered-btn');
  if (filterInput) {
    filterInput.addEventListener('input', function() {
      var query = this.value.toLowerCase().trim();
      document.querySelectorAll('#book-checklist li').forEach(function(li) {
        var label = li.querySelector('label');
        var text = label ? label.textContent.toLowerCase() : '';
        li.style.display = (!query || text.indexOf(query) !== -1) ? '' : 'none';
      });
      if (selectFilteredBtn) selectFilteredBtn.hidden = !query;
    });
  }

  if (selectFilteredBtn) {
    selectFilteredBtn.addEventListener('click', function() {
      document.querySelectorAll('#book-checklist li').forEach(function(li) {
        var cb = li.querySelector('input[type="checkbox"]');
        if (cb) cb.checked = (li.style.display !== 'none');
      });
    });
  }

  // ——— Select All / Deselect All ———
  var selectAllBtn = document.getElementById('select-all-btn');
  var deselectAllBtn = document.getElementById('deselect-all-btn');

  if (selectAllBtn) {
    selectAllBtn.addEventListener('click', function() {
      document.querySelectorAll('#book-checklist input[type="checkbox"]').forEach(function(cb) {
        cb.checked = true;
      });
    });
  }

  if (deselectAllBtn) {
    deselectAllBtn.addEventListener('click', function() {
      document.querySelectorAll('#book-checklist input[type="checkbox"]').forEach(function(cb) {
        cb.checked = false;
      });
    });
  }

})();
</script>
