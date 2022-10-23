export function test() {
  console.log("Hello");
}

export function askForDelete(recipeId: number) {
  console.log("Deleting recipe: ", recipeId);
  if (confirm("Are you sure you want to delete this recipe?!!")) {
    window.location.href=`/recipes/delete/${recipeId}`;
  }
}