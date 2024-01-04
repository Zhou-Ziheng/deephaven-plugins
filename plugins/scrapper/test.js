var json = require("./docs/documentation.json");

const parse(child) => {
  
}

for (i = 0; i < json.children.length; i++) {
  console.log(json.children[i].name);

  child = json.children[i].children;
  for (j = 0; j < child.length; j++) {
    console.log(child[j].name);
  }
}
