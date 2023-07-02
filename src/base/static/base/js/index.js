import { Application } from "@hotwired/stimulus";

import themeHandler from "./controllers/themeHandler";
import contentParser from "./controllers/contentParser";

window.Stimulus = Application.start();

Stimulus.register("theme-handler", themeHandler);
Stimulus.register("content-parser", contentParser);

Stimulus.debug = "__APP_ENV__" === "development";
