
function addIngredient() {

    let newCounterValue = parseInt(document.getElementById("ingredientCounter").value) + 1;
    const newInput = document.createElement("input");
    newInput.id = 'ingr' + newCounterValue;
    newInput.setAttribute("type", "text");
    newInput.setAttribute("name", "ingredient")
    let container = document.getElementById("addedIngredients");
    container.append(newInput);
    document.getElementById("ingredientCounter").value = newCounterValue;
    console.log("RADIM")

};

var el = document.getElementById("addIngredient")
if (el) {
    el.addEventListener("click", () => {
        addIngredient();
    });
};

