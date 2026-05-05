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

  <!-- Format selector -->
  <div class="print-hub-section">
    <h2>Page Format</h2>
    <div class="format-selector" role="group" aria-label="Page format">
      <span class="format-label">Size:</span>
      <button class="format-btn" data-format="letter">Letter</button>
      <button class="format-btn" data-format="a4">A4</button>
      <button class="format-btn" data-format="69">6×9″</button>
    </div>
  </div>

  <!-- Individual essays -->
  {% assign show_individual = site.data.theme.print.show-individual | default: true %}
  {% if show_individual != false %}
  <div class="print-hub-section">
    <h2>Essays</h2>
    <div class="tributary-cards">
      {% assign sorted_essays = site.essay | sort: "order" %}
      {% for essay in sorted_essays %}
      <div class="tributary-card">
        <p class="card-title">{{ essay.title }}</p>
        <a class="card-link" href="{{ '/print/book/' | relative_url }}?essays={{ essay.slug }}" data-essay="{{ essay.slug }}" target="_blank">
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

  <!-- Book builder -->
  {% assign show_book = site.data.theme.print.show-book | default: true %}
  {% if show_book != false %}
  <div class="print-hub-section">
    <h2>Build the Book</h2>
    <div class="book-builder">
      <ul class="book-checklist" id="book-checklist">
        {% for essay in sorted_essays %}
        <li>
          <input type="checkbox" id="book-{{ essay.slug }}" value="{{ essay.slug }}" checked>
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

</div>

<script>
(function() {
  // ——— Format selector ———
  var storedFormat = localStorage.getItem('print-format') || 'letter';

  document.querySelectorAll('.format-btn').forEach(function(btn) {
    if (btn.dataset.format === storedFormat) btn.classList.add('active');
    btn.addEventListener('click', function() {
      var fmt = this.dataset.format;
      localStorage.setItem('print-format', fmt);
      document.querySelectorAll('.format-btn').forEach(function(b) {
        b.classList.toggle('active', b.dataset.format === fmt);
      });
      storedFormat = fmt;
      updateEssayLinks(fmt);
    });
  });

  function updateEssayLinks(fmt) {
    document.querySelectorAll('.card-link[data-essay]').forEach(function(link) {
      var slug = link.dataset.essay;
      var base = '{{ "/print/book/" | relative_url }}';
      link.href = base + '?essays=' + slug + '&format=' + fmt;
    });
  }

  // Set initial format on links
  updateEssayLinks(storedFormat);

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

      var fmt = localStorage.getItem('print-format') || 'letter';
      var baseUrl = '{{ "/print/book/" | relative_url }}';
      window.open(baseUrl + '?essays=' + checked.join(',') + '&format=' + fmt, '_blank');
    });
  }

})();
</script>
