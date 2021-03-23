
function injectResultData(statement, data){

    document.getElementById("statementText").innerHTML = statement
    document.getElementById("snopesRating").innerHTML = data.rating
    document.getElementById("whatsTrue").innerHTML = data.true
    document.getElementById("whatsFalse").innerHTML = data.false
    document.getElementById("snopesLink").innerHTML = data.snopes
    document.getElementById("wiki").innerHTML = data.wiki
    document.getElementById("snopesLink").href = data.snopes
    document.getElementById("wiki").href = data.wiki
}
