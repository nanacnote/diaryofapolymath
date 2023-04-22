import { Controller } from "@hotwired/stimulus";

const KEY = "diary-of-a-polymath-theme";

export default class extends Controller {
  connect() {
    document.body.classList.add(localStorage.getItem(KEY) || "theme-light");
  }

  toggle(_e) {
    document.body.classList.toggle("theme-dark");
    document.body.classList.toggle("theme-light");
    localStorage.setItem(
      KEY,
      localStorage.getItem(KEY) === "theme-dark" ? "theme-light" : "theme-dark"
    );
  }
}
