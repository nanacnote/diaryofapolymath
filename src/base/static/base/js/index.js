import { Application } from "@hotwired/stimulus";

import theme from "./controllers/theme";

window.Stimulus = Application.start();

Stimulus.register("theme", theme);

Stimulus.debug = "__APP_ENV__" === "development";
