# frozen_string_literal: true

#########
#
# Scrolly Block Check, v1.0
#
# Jekyll plugin that verifies essay/feature/scrolly-media.html,
# scrolly-step.html, and scrolly-end.html were paired correctly on each
# essay page. Those includes cooperatively hand-balance raw <div> tags
# across a Markdown file (open a block, add panels, close the block);
# nothing at the Liquid template level can detect a block left open when
# an essay simply ends without a closing scrolly-end.html, since that
# case has no later include call to trigger a self-heal. This plugin
# inspects the fully rendered HTML instead, where that limitation
# doesn't apply.
#
# Two independent checks per essay document:
#   1. Imbalance — more scrolly-section opens than closes means a block
#      was left open at the end of the essay.
#   2. Warning marker — the includes render a visible ".scrolly-block-warning"
#      banner whenever they detect a nested/orphaned/stray block or a
#      missing image; its presence means something needed correcting.
#
# Always logs a console warning naming the file so authors see it during
# `jekyll serve`/`jekyll build`, without interrupting local iteration.
# Raises a fatal build error in production builds (JEKYLL_ENV=production)
# so a broken scrolly block can never silently ship — mirrors this
# project's existing `jekyll.environment == "production"` gating.
#
#########

Jekyll::Hooks.register :documents, :post_render do |doc|
  next unless doc.collection.label == "essay"
  next unless doc.output

  open_count = doc.output.scan(/class="scrolly-section/).length
  closed_count = doc.output.scan(/scrolly-exit/).length
  has_warning = doc.output.include?("scrolly-block-warning")

  next if open_count <= closed_count && !has_warning

  reasons = []
  reasons << "#{open_count - closed_count} scrolly block(s) left open (missing scrolly-end.html)" if open_count > closed_count
  reasons << "a scrolly block warning was rendered (nested/orphaned/stray include, or a missing image)" if has_warning

  message = "#{doc.relative_path}: #{reasons.join('; ')}. Check the scrolly-media.html / scrolly-step.html / scrolly-end.html includes in this essay."

  if Jekyll.env == "production"
    raise Jekyll::Errors::FatalException, "Scrolly block error — #{message}"
  else
    Jekyll.logger.warn "Scrolly:", message
  end
end
