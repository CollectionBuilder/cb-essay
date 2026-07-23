/*
    Build popup HTML for a scrolly-map marker from a GeoJSON feature.
    Mirrors the popup template used by the full collection map (js/map-js.html),
    sourced from the same _data/config-map.csv field config.
    Depends on getIcon() (helpers/get-icon.js) for the icon-thumb fallback.
*/
function getMapPopup(feature) {
    function escapeHtml(str) {
        return String(str).replace(/[&<>"']/g, function (ch) {
            return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch];
        });
    }

    var props = (feature && feature.properties) ? feature.properties : {};
    var itemHref = `{{ '/items/' | relative_url }}${ props.parent ? props.parent + ".html#" + props.id : props.id + ".html" }`;
    var title = escapeHtml(props.title || '');
    var imgAlt = escapeHtml(props.alt ? props.alt : (props.title || ''));
    var thumbImg;
    if (props.img) {
        thumbImg = '<img class="map-thumb" src="' + props.img + '" alt="' + imgAlt + '">';
    } else {
        thumbImg = getIcon(props.template, props.format, "thumb");
    }
    var popupTemplate = '<h2 class="h4"><a class="text-dark" href="' + itemHref + '">' +
        title + '</a></h2><div class="text-center"><a href="' + itemHref +
        '" >' + thumbImg + '</a></div><p>';
    {% assign _map_popup_fields = site.data.config-map %}{% for f in _map_popup_fields %}{% if f.display_name %}
    if (props[{{ f.field | escape | jsonify }}]) {
        popupTemplate += '<strong>{{ f.display_name }}:</strong> ' + escapeHtml(props[{{ f.field | escape | jsonify }}]) + '<br>';
    }
    {% endif %}{% endfor %}
    popupTemplate += '</p><div class="text-center"><a class="btn btn-light" href="' + itemHref + '" >View Item</a></div>';
    return popupTemplate;
}
