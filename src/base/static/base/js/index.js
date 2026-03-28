import { Application } from "@hotwired/stimulus";

import commentReply from "./controllers/commentReply";
import contentParser from "./controllers/contentParser";

window.Stimulus = Application.start();

Stimulus.register("content-parser", contentParser);
Stimulus.register("comment-reply", commentReply);

Stimulus.debug = "__APP_ENV__" === "development";
