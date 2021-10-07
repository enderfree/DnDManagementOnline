function AddInv(){
	var newInv = document.createElement("fieldset");
	newInv.innerHTML = document.getElementById("anInventory").innerHTML;
	newInv.style = "display: inline";
	
	document.getElementById('inventories').appendChild(newInv);
}

function validateAndSend(){
	var isValid = true;
	
	if(document.getElementById('charName').value != ""){
		var regex = /^[0-9]+$/;
		if(regex.test(document.getElementById('str').value)){
			if(regex.test(document.getElementById('speed').value)){
				//inventories
				var invNames = document.getElementsByClassName("invName");
				for(var i = 0; i < invNames.length; ++i){
					if(invNames.item(i).value != ""){
						if(invNames.item(i).value == document.getElementById('charName').value){
							isValid = false;
							alert("Character and inventories must have different names!");
							break;
						}
					}
					else{
						isValid = false;
						alert('"Name" is always a required field!');
						break;
					}
					
					for(var j = 0; j < invNames.length; ++j){
						if(invNames.item(i).value == invNames.item(j).value && i != j){
							isValid = false;
							alert('Inventories must have different names! ');
							break;
						}
					}
					
					if(!isValid){
						break;
					}
				}
			}
			else{
				isValid = false;
				alert('Your base speed is mendatory and must contain numbers only. ');
			}
		}
		else{
			isValid = false;
			alert('Your strength score is mendatory and must contain numbers only. ');
		}
	}
	else{
		isValid = false;
		alert('"Name" is always a required field!');
	}
	
	if(isValid){
		//I coded based on false assumptions so I had to comment a lot of lines
		
		////store inventories values before submitting (by default, only the latest will be submitted)
		//var fieldsArray = [document.getElementsByClassName("invName"), document.getElementsByClassName("invBg"), document.getElementsByClassName("invFontColor"), document.getElementsByClassName("maxCapacity"), document.getElementsByClassName("isCarried"), document.getElementsByClassName("items")];
		
		////variable initialisation (so I can use += and have the good values)
		////I get by name because this is the one that will be sent by my form
		//var resultArray = [document.getElementsByName("invName"), document.getElementsByName("invBg"), document.getElementsByName("invFontColor"), document.getElementsByName("maxCapacity"), document.getElementsByName("isCarried"), document.getElementsByName("items")]
		//for(var i = 0; i < resultArray.length; ++i){
		//	resultArray[i].value = "";
		//}
		
		//for(var i = 0; i < fieldsArray.length; ++i){
		//	for(var j = 0; j < fieldsArray[i].length; ++j){
		//		//alert(fieldsArray[i].item(j).value);
		//		resultArray[i].value += fieldsArray[i].item(j).value; //resultArray and fieldsArray should have the same size
		//		resultArray[i].value += ","
		//	}
		//}
		
		document.getElementsByTagName("form").item(0).submit();
	}
}