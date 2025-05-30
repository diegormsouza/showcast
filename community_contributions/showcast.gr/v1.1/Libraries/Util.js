const util = (() => {
    //like set interval but start at 0
    const startInterval = (callback, millisec) => {
        callback();
        return setInterval(callback, millisec);
    }

    let createCategoryButton = (area, text) => {
        let cbItem = document.createElement('button');
        cbItem.className = "btn btn-secondary";
        cbItem.setAttribute('area', area);
        cbItem.innerHTML = text;
        return cbItem;
    }

    let createGroupBaseButtons = (id, items, callback, isVertical = false) => {
        let groupBaseButtons = [].concat(items || []);
        //create
        let group = document.createElement('div');
        //edit group

        let mainClass = 'btn-group';
        if (isVertical) mainClass += '-vertical';

        group.className = mainClass + " area-btn w-100 p-2";
        group.setAttribute('role', 'group');
        group.id = id;
        //assemble
        groupBaseButtons.forEach((item, index) => {
            item.addEventListener('click', event => {
                if (!item.classList.contains('active')) {

                    let targetSiblings = Array.from(item.parentElement.children);
                    for (let elem of targetSiblings) {
                        if (elem.classList.contains('active')) elem.classList.remove('active');
                    }
                    item.classList.add('active');

                    callback(item.getAttribute('area'));
                }
            });
            group.appendChild(item);
        })
        return group;
    }

    let TimeService = {
        async getServerTime() {
            let time = await fetch(`${paths.backend}/getServerTime.php`, { method: "GET" })
                .then(response => response.json())
                .then(srvTimeJSON => new Date(srvTimeJSON.time));
            return time;
        },

        displayUTC(selector, time = new Date()) {
            const timerElem = document.querySelector(selector);
            const interval = 1000; // ms
            let expected = Date.now() + interval;
            setTimeout(step, interval);
            function step() {
                let dt = Date.now() - expected; // the drift (positive for overshooting)
                if (dt > interval) {
                    console.log("Unexpected, maybe the browser was inactive?");
                    // TimeService.getServerTime()
                    //     .then(srvTime => {util.TimeService.displayUTC(selector, srvTime);});
                }
                time.setSeconds(time.getUTCSeconds() + 1);
                timerElem.textContent = (("0" + time.getUTCHours()).slice(-2) + ':' + ("0" + time.getUTCMinutes()).slice(-2) + ':' + ("0" + time.getUTCSeconds()).slice(-2));
                expected += interval;
                setTimeout(step, Math.max(0, interval - dt)); // take into account drift
            }
        }
    };


    let objectCompareKeys = (obj1, obj2) => {
        return arraysMatch(Object.keys(obj1), Object.keys(obj2));
    }

    let arraysMatch = (arr1, arr2) => {
        // Check if the arrays are the same length
        if (arr1.length !== arr2.length) return false;
        // Check if all items exist and are in the same order
        for (let i = 0; i < arr1.length; i++) { if (arr1[i] !== arr2[i]) return false; }
        // Otherwise, return true
        return true;
    };

    //img html element with a src as parameter
    let getImgOrientation = img => {
        img.addEventListener("load", () => {
            if (img.naturalHeight > img.naturalWidth) return 'portrait';
            else if (img.naturalHeight < img.naturalWidth) return 'landscape';
            else return 'square';
        })
    }

    let findFileUrls = async (folderUrl, fileTypes = "all", isLocal = true) => {
        let response = await fetch(`../PHP/getDirContents.php`, {
            method: 'post',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
//                'Content-Type': 'text'
            },
            body: JSON.stringify({ folderUrl: folderUrl, isLocal: isLocal, fileTypes: fileTypes })
        });
        let respJson = await response.json();
//        let respJson = await response.text();
//        console.log("response: ");
//        console.log(respJson);
        return respJson;
    }

    const findAncestor = (element, parentSelector) => {
        function collectionHas(a, b) { //helper function
            for (var i = 0, len = a.length; i < len; i++) {
                if (a[i] == b) return true;
            }
            return false;
        }
        let all = document.querySelectorAll(parentSelector);
        let cur = element.parentNode;
        while (cur && !collectionHas(all, cur)) {
            cur = cur.parentNode;
        }
        return cur;
    }

    const setCookie = (name, value, maxAgeHours) => {
        let maxAgeSeconds = maxAgeHours * 60 * 60;
        document.cookie = `${name}=${value};max-age=${maxAgeSeconds};`;
    }

    const deleteCookie = (name) => {
        document.cookie = `${name}=;expires=0;`;
    }

    const readRemoteTextFile = async (url) => {
        let response = await fetch(url, {
            method: 'get',
            mode: 'cors'
        })
        response = await response.blob();
        //return response;
        let fileReader = new FileReader();
        fileReader.readAsText(response, 'windows-1253');
        return fileReader;
    }

    const openFullscreen = (elem) => {
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.mozRequestFullScreen) { /* Firefox */
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
            elem.webkitRequestFullscreen();
        } else if (elem.msRequestFullscreen) { /* IE/Edge */
            elem.msRequestFullscreen();
        }
    }

    const closeFullscreen = () => {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.mozCancelFullScreen) { /* Firefox */
          document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
          document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { /* IE/Edge */
          document.msExitFullscreen();
        }
      }

    function Refresh() {
        let interval = null;

        this.set = (fn, rate) => {
            if (interval) clearInterval(interval);
            interval = util.startInterval(fn, rate);
        };

        this.clear = () => {
            if (interval) clearInterval(interval);
        };
    }

    return {
        startInterval: startInterval,
        createCategoryButton: createCategoryButton,
        createGroupBaseButtons: createGroupBaseButtons,
        TimeService: TimeService,
        findAncestor: findAncestor,
        objectCompareKeys: objectCompareKeys,
        arraysMatch: arraysMatch,
        getImgOrientation: getImgOrientation,
        findFileUrls: findFileUrls,
        setCookie: setCookie,
        deleteCookie: deleteCookie,
        readRemoteTextFile: readRemoteTextFile,
        openFullscreen: openFullscreen,
        closeFullscreen: closeFullscreen,
        Refresh: Refresh
    }
})()
