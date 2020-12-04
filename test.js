const fetch = require("node-fetch");

fetch(
  "http://localhost:5000/process" +
    "?" +
    new URLSearchParams({
      date1: "27/01/2015",
      date2: "28/01/2016",
    })
).catch(console.log());
