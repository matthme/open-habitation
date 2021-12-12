import { getHouseInfo } from "./fetchers.js";

const HOUSE_QUERY_URL = "../resources/houseinfo.json"

// console.log(new Date().toISOString());

let rows: string[] = []; // rows of the table

const buttonEl = document.querySelector("#search_button")!;
const tbodyEl = document.querySelector("tbody")!;

function houseQuery(e: Event) {
    // e.preventDefault();
    getHouseInfo(HOUSE_QUERY_URL).then((info: { [key: string]: any } ) => {

        tbodyEl.innerHTML = "";

        if (rows.length >= 10) {
            rows.pop()
        }

        let newrow: string = "<tr>";

        Object.keys(info).forEach( (k, i) => {
            newrow += `<td>${info[k]}</td>`
        })

        newrow += "</tr>";

        rows.push(newrow);

        rows.forEach(row => {
            tbodyEl.innerHTML += row;
        })

    }).catch(err => {
        console.log("No info found for that house.")
    })

}

buttonEl.addEventListener("click", houseQuery);

// if(button){
//     button.addEventListener("click", houseQuery);
// }







// const getProduction = (url="../resources/production.json") => {

//     getResource(url).then(data => {
//         return data
//     }).catch(err => {
//         console.log(err)
//     })
// }


// getResource("../resources/production.json").then(data => {
//     console.log(data);
// }).catch(err => {
//     console.log(err)
// })

// fetch("../resources/production.json").then((response) => {
//     if(response.status===200){
//         return response.json()
//     } else {
//         throw new Error("cannot fetch data.");
//     }
// }).then((data) => {
//     console.log(data);
// }).catch((err) => {
//     console.log(err);
// })

