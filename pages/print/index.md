---
layout: print-hub
title: Print & PDF
permalink: /print/
sitemap: false
search_exclude: true
---

<div class="print-hub">

  <div class="print-hub-header">
    <h1>Print &amp; PDF</h1>
    <p>Print individual essays or build a custom PDF book from the full collection.</p>
  </div>

  <!-- Featured essay (shown via JS when ?essay= URL param is present) -->
  <div class="print-hub-featured" id="print-featured" aria-live="polite">
    <p class="featured-label">Print This Essay</p>
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
    <h2>Build the Book</h2>
    <div class="book-builder">
      <input class="book-filter" id="chapter-filter" type="search" placeholder="Filter chapters…" aria-label="Filter chapter list" autocomplete="off">
      <div class="book-controls">
        <button class="book-control-btn" id="select-all-btn">Select All</button>
        <button class="book-control-btn" id="deselect-all-btn">Deselect All</button>
        <button class="book-control-btn" id="select-filtered-btn" hidden>Select All Filtered</button>
      </div>
      <ul class="book-checklist" id="book-checklist">
        {% for essay in sorted_essays %}{% assign url_key = essay.url | split: "/" | last | remove: ".html" %}
        <li>
          <input type="checkbox" id="book-{{ essay.slug }}" value="{{ essay.slug }}" data-url-key="{{ url_key }}" checked>
          <label for="book-{{ essay.slug }}">{{ essay.title }}</label>
        </li>
        {% endfor %}
      </ul>
      <button class="book-generate-btn" id="book-generate-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" viewBox="0 0 16 16" style="margin-right:0.4rem;">
          <path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/>
          <path d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/>
        </svg>
        Generate Book PDF
      </button>
    </div>
  </div>
  {% endif %}

  <!-- Individual essays -->
  {% assign show_individual = site.data.theme.print.show-individual | default: true %}
  {% if show_individual != false %}
  <div class="print-hub-section">
    <h2>Essays</h2>
    <div class="tributary-cards">
      {% for essay in sorted_essays %}
      <div class="tributary-card">
        <p class="card-title">{{ essay.title }}</p>
        <a class="card-link" href="{{ '/print/book/' | relative_url }}?essays={{ essay.slug }}" target="_blank">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" viewBox="0 0 16 16">
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

  // ——— URL param: ?essay=url-key ———
  var params = new URLSearchParams(window.location.search);
  var featuredUrlKey = params.get('essay');

  if (featuredUrlKey && essayTitles[featuredUrlKey]) {
    var block = document.getElementById('print-featured');
    var titleEl = document.getElementById('featured-title');
    var btn = document.getElementById('featured-print-btn');

    // Resolve url-key → essay.slug via the checkbox data-url-key attribute.
    // print.html filters by data-essay="{{ essay.slug }}", so the ?essays= param
    // must use essay.slug (not the url-key which may differ for dotted filenames).
    var matchingCb = document.querySelector('#book-checklist input[data-url-key="' + featuredUrlKey + '"]');
    var essaySlug = matchingCb ? matchingCb.value : featuredUrlKey;

    titleEl.textContent = essayTitles[featuredUrlKey];
    btn.href = '{{ "/print/book/" | relative_url }}' + '?essays=' + essaySlug;
    block.style.display = 'block';

    // Pre-check only this essay in the book builder
    document.querySelectorAll('#book-checklist input[type="checkbox"]').forEach(function(cb) {
      cb.checked = (cb.dataset.urlKey === featuredUrlKey);
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

      window.open('{{ "/print/book/" | relative_url }}' + '?essays=' + checked.join(','), '_blank');
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
