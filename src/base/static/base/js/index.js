import { Application } from "@hotwired/stimulus";

import contentParser from "./controllers/contentParser";

window.Stimulus = Application.start();

Stimulus.register("content-parser", contentParser);

Stimulus.debug = "__APP_ENV__" === "development";
