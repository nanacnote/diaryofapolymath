import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static targets = [
    "indicator",
    "indicatorText",
    "indicatorSnippet",
    "submittedMessage",
    "errorMessage",
  ];

  connect() {
    this.form = this.element.querySelector("#post-comment-form");
    // parent input is the hidden input in the comment form that holds the ID of the comment being replied to (if any)
    this.parentInput = this.element.querySelector("#id_parent");

    const hasSubmittedMessage =
      this.hasSubmittedMessageTarget && this.isVisible(this.submittedMessageTarget);
    const hasVisibleErrors =
      this.hasErrorMessageTarget && this.errorMessageTargets.some((node) => this.isVisible(node));

    if (this.form && (hasSubmittedMessage || hasVisibleErrors)) {
      this.form.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    if (!this.parentInput || !this.hasIndicatorTarget) {
      return;
    }

    if (!this.parentInput.value) {
      this.indicatorTarget.hidden = true;
    }

  }

  isVisible(element) {
    return !!(element && !element.hidden && element.getClientRects().length);
  }

  select(event) {
    const link = event.currentTarget;
    const replyTo = link.getAttribute("data-reply-to");
    const replyAuthor = link.getAttribute("data-reply-author") || "this comment";
    const replySnippet = link.getAttribute("data-reply-snippet") || "";

    if (!this.parentInput) {
      return;
    }

    this.parentInput.value = replyTo || "";
    this.indicatorTextTarget.textContent = `Replying to ${replyAuthor}`;
    this.indicatorSnippetTarget.textContent = replySnippet ? `"${replySnippet}"` : "";
    this.indicatorTarget.hidden = false;
  }

  clear(event) {
    event.preventDefault();

    if (!this.parentInput) {
      return;
    }

    this.parentInput.value = "";
    this.indicatorTextTarget.textContent = "";
    this.indicatorSnippetTarget.textContent = "";
    this.indicatorTarget.hidden = true;
  }
}
