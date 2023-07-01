import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  connect() {
    const content = this.element.textContent;
    const parsedContent = content;

    // TODO: handle parsing here

    this.element.innerHTML = parsedContent;
  }
}
