// function add(num1, num2){
//     return num1 + num2;
// }
//
//
// function myReduce(arr, myFunc){
//     let emptyArr= [];
//     for (let i = 0; i < arr.length; i++){
//         let result = myFunc(arr[i], arr[i + 1])
//         emptyArr.push(result)
//     }
//     return emptyArr
// }
//
//
// let x = myReduce([1, 2, 3, 4, 5], add)
// console.log(x)

function add(num1, num2){
    return num1 + num2;
}


function myReduce(arr, myFunc){
    let emptyArr= [];
    for (let i = 0; i < arr.length; i++){
        let result = myFunc(arr[i], arr[i + 1])
        emptyArr.push(result)
    }
    return emptyArr
}


let x = myReduce([1, 2, 3, 4, 5], add)
console.log(x)
