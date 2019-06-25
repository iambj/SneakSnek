/*

	TODO:
		- Add stop/start button
		x Add custom intervals
		x Watcher for static files.
		- Watch for folders (this should be done with handlers and watchdog)
		- Add config window
		- Inject css for real (probably should use JSON) ?
		- Ability to reset the changeRate
*/
let enabled = true;
let refreshWithoutChange = false;
let refreshRate = 1500; // Default refresh rate in ms.
let changeRate = 1.1;
let adaptiveRate = true
let refreshFailed = 0;


const refreshPoint = "http://localhost:5000/check_changes"
const params = {
	'method' : 'POST',
	'body' : null
}



function refresh(data) {
	/*
		if json data changed and static files set to css
			request just css and inject
		if json data changed and static files set to js
			request just js and inject? can you even do this?
		if just json data changed time or no static files
			refresh whole page
	*/
	if (data !== "same" || refreshWithoutChange === true) {
		console.log("Refreshing");
		localStorage.setItem("serverUpdate", data);
		location.reload(true)
	} else if (adaptiveRate && refreshFailed > 10){
		console.warn("Increasing refresh delay.")
		refreshFailed = 0
		refreshRate = (Math.floor(changeRate * refreshRate))
	}else{
		console.log("No refresh needed.")
		refreshFailed ++;
	}
}

var refresher = () => {
	if (enabled === false && refreshWithoutChange !== true){
		return;
	}
	let last = ""
	if (localStorage.getItem("serverUpdate")) {
		last = localStorage.getItem("serverUpdate");
	} 
	console.log("Attempting Refresh" , `(${refreshRate})`, Date.now());
	params.body = last
	fetch(refreshPoint, params)
		 .then(res => res.text())
		 .then(info => {
			 refresh(info)
			 refreshLoop = setTimeout(refresher, refreshRate)
		})
}

var refreshLoop = setTimeout(refresher, refreshRate)


function stopRefreshing(){
	clearTimeout(refreshLoop)
}

function startRefreshing() {
	refreshLoop = setTimeout(refresher, refreshRate)
}
