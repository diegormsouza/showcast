'use strict';

(() => {


    //------

    let areaButtonsContainer = document.querySelector('#areaButtonsContainer');
    let userviewActivate = document.querySelector('#userview-activate');
    let userviewControls = document.querySelector('#userview-controls');
    let imageCaptions = document.querySelectorAll('tr:nth-child(odd) > td');
    let userviewSelectedImagesNumber = document.querySelector('#userview-selected-images-num');
    let userviewVisibleList = document.querySelector('#userview-visible-list');
    let userviewEnterButton = document.querySelector('#userview-enter');
    let groupThumbDivsButtons = document.getElementsByClassName("thumb_div");

    let userviewSelectionsList = new Array();
    for (let i = 0; i < 4; i++)
        userviewSelectionsList[i] = new Array();

    let handlersUserview = [];
    let userviewIndex = 0;
    let addUserviewButtons = document.getElementsByClassName("add-userview-button");

    let areaButtons = [];
    let areas = ['FDK', 'EU', 'GR'];
    let areas_texts = ['FDK', 'EUR', 'GRC'];
    let selectedArea = 'FDK';

    for (let i = 0; i < areas.length; i++)
        areaButtons.push(util.createCategoryButton(areas[i], areas_texts[i]));

    let groupAreaButtons = util.createGroupBaseButtons('area-group-btn', areaButtons, clickedElem => {
        setArea(clickedElem);
    });

    areaButtonsContainer.appendChild(groupAreaButtons);
    areaButtons[0].classList.add('active');



    function setArea(newArea) //Replace all old area labels with the new one in all URLs
    {
        if (selectedArea != newArea) {
          for (let i = 0; i < groupThumbDivsButtons.length; i++) {
            let a_href = groupThumbDivsButtons[i].querySelector("a").href;
            a_href = a_href.replace('area=' + selectedArea, 'area=' + newArea);
            groupThumbDivsButtons[i].querySelector("a").href=a_href;
            let img_src = groupThumbDivsButtons[i].querySelector("img").src;
            img_src = img_src.replace('_' + selectedArea + '_', '_' + newArea + '_');
            groupThumbDivsButtons[i].querySelector("img").src = img_src;
          };

          selectedArea = newArea;
        }
    }

    //------

    let satButtonsContainer = document.querySelector('#satButtonsContainer');
    let satPanels = document.querySelectorAll('#main-panel > div');

    let sats_ids = ['msg', 'msg-rss', 'msg-iodc', 'sst', 'wmo']
    let sats_texts = ['MSG (0&#176;)', 'MSG-RSS (9.5&#176;)', 'MSG-IODC (41.5&#176;)' , 'SST', 'WMO']
    let satButtons = [];

    for (let i = 0; i < sats_ids.length; i++)
        satButtons.push(util.createCategoryButton(sats_ids[i], sats_texts[i]));

    let groupSatButtons = util.createGroupBaseButtons('sat-group-btn', satButtons, clickedElem => {
        showSat(clickedElem);
          //--------- onclick event listener for msg-rss button to set area to EU -----------------------------------
        document.querySelector("[area='msg-rss']").onclick = function() {
            areaButtons[1].click();
        };
        //--------- onclick event listener for msg-iodc button to set area to GR -----------------------------------
        document.querySelector("[area='msg-iodc']").onclick = function() {
            areaButtons[2].click();
        };
        //--------- onclick event listener for wmo button to open  Player_wmo.html -----------------------------------
        document.querySelector("[area='wmo']").onclick = function() {
            window.open("../HTML/Player_wmo.html");
            satButtons[0].click();
        }
    }, true);

    satButtonsContainer.appendChild(groupSatButtons);
    satButtons[0].click();

    function showSat(sat) {
        for (let i = 0; i < satPanels.length; i++) {
            if (satPanels[i].id == sat) {
                satPanels[i].classList.remove('d-none');
                satPanels[i].classList.add('d-block');
            }
            else {
                if (!$(satPanels[i]).hasClass('d-none')) {
                    satPanels[i].classList.remove('d-block');
                    satPanels[i].classList.add('d-none');
                }
            }
        }
    }

    //------

    userviewActivate.addEventListener('click', () => {
        let enable = !$(userviewActivate).hasClass('active');
        $('.userview-info').tooltip('hide');

        toogleUserviewControls(enable);
        toogleUserviewListeners(enable);

        if (enable) {
            userviewActivate.classList.add('active');
            userviewActivate.textContent="Deactivate UserView";
            for (let i = 0; i < addUserviewButtons.length; i++)
				addUserviewButtons[i].style.visibility="visible";
		}
        else {
            userviewActivate.classList.remove('active');
            userviewActivate.textContent="Activate UserView";
			for (let i = 0; i < addUserviewButtons.length; i++)
				addUserviewButtons[i].style.visibility="hidden";
		}
    });

    function toogleUserviewControls(enable) {
        if (enable) {
            userviewControls.classList.remove('d-none');
            userviewControls.classList.add('d-block');
        }
        else {
            userviewControls.classList.remove('d-block');
            userviewControls.classList.add('d-none');
        }
    }

    function toogleUserviewListeners(enable) {
        if (enable) {
            for (let i = 0; i < imageCaptions.length; i++) {
                imageCaptions[i].addEventListener('click', handlersUserview[i] = (event) => userviewSelection(event));
            }
        }
        else {
            for (let i = 0; i < handlersUserview.length; i++) {
                imageCaptions[i].removeEventListener('click', handlersUserview[i]);
            }
        }
    }

    function userviewSelection(event) {
        //Find the position of the clicked cell in its row
        let captionElem = event.target;
        let parentCellElem = captionElem.closest('td');
        let parentRow = parentCellElem.closest('tr');
        let parentIndex = Array.prototype.indexOf.call(parentRow.children, parentCellElem);

        //Find the corresponding image of the cell (visually it's just above it), and get its link
        let previousRow = parentRow.previousElementSibling;
        let correspondingLink = previousRow.querySelectorAll('td').item(parentIndex).querySelector('a').href;

        let parameters = (new URL(correspondingLink)).searchParams;

        let cat = parameters.get('cat');
        let type = parameters.get('type');
        let area = parameters.get('area');

        let hasSelection = false;
        let hasSpace = true;

        for (let i = 0; i < userviewSelectionsList[0].length; i++) {
            if (userviewSelectionsList[0][i] == cat && userviewSelectionsList[1][i] == type && userviewSelectionsList[2][i] == area) {
                hasSelection = true;
            }
        }

        userviewSelectionsList[0].length = userviewSelectionsList[0].length;

        if (userviewSelectionsList[0].length >= 4 && !hasSelection) {
            hasSpace = false;
            lightUpText(userviewSelectedImagesNumber);
        }

        let state;
        if (hasSelection)
            state = 'exists';
        else if (hasSpace)
            state = 'add';
        else
            state = 'full';

        lightUpCell(parentCellElem, state); //Briefly point out to the selected cell and indicate if it could be added

        if (!hasSelection && hasSpace) {
            userviewVisibleList.appendChild(
                createUserviewListRow(cat, type, area, userviewIndex));

            userviewSelectionsList[0].push(cat);
            userviewSelectionsList[1].push(type);
            userviewSelectionsList[2].push(area);
            userviewSelectionsList[3].push(userviewIndex);
        }

        userviewIndex++;

        if (userviewSelectionsList[3].length > 0) userviewEnterButton.disabled = false;

        userviewSelectedImagesNumber.innerHTML = userviewSelectionsList[0].length;
    }

    function createUserviewListRow(cat, type, area, index) {
        let container = document.createElement('div');
        container.setAttribute('index', index);

        let label = document.createElement('label');
        label.classList.add('highlight');
        label.innerHTML = cat + ' / ' + type + ' / ' + area;

        let removeBtn = document.createElement('label');
        removeBtn.classList.add('remove');
        removeBtn.innerHTML = '<i class="fas fa-minus-circle"></i>'
        removeBtn.addEventListener('click', () => {
            removeUserviewSelection(index);
        });

        container.appendChild(label);
        container.appendChild(removeBtn);

        return container;
    }

    function removeUserviewSelection(index) {

        let row = document.querySelector('div[index="' + index + '"]');
        row.remove();

        for (let i = 0; i < userviewSelectionsList[3].length; i++) {
            if (userviewSelectionsList[3][i] == index) {
                for (let j = 0; j < userviewSelectionsList.length; j++)
                    userviewSelectionsList[j].splice(i, 1);
            }
        }

        if (userviewSelectionsList[3].length == 0) userviewEnterButton.disabled = true;

        userviewSelectedImagesNumber.innerHTML = userviewSelectionsList[0].length;
    }


    function lightUpCell(elem, state) {
        let initialBackgroundColor = elem.style.backgroundColor;

        if (state == 'full') {
            elem.style.backgroundColor = '#8a0000'; //shade of red
        }
        else if (state == 'add') {
            elem.style.backgroundColor = "#00f1c9"; //--theme-color-lively

        }
        else if (state == 'exists') {
            elem.style.backgroundColor = "#005263"; //--theme-color-light
        }

        setTimeout(function () {
            elem.style.backgroundColor = initialBackgroundColor;
        }, 100);
    }

    function lightUpText(elem) {
        let initialWeight = elem.style.fontWeight;
        let initialColor = elem.style.color;

        elem.style.fontWeight = "bolder";
        elem.style.color = "red";

        setTimeout(function () {
            elem.style.fontWeight = initialWeight;
            elem.style.color = initialColor;
        }, 200);
    }

    userviewEnterButton.addEventListener('click', () => {
        //todo: create cookie

        const a = document.createElement("a");
        a.target = '_blank';

        a.href = '../HTML/UserView.html?';

        for (let i = 0; i < userviewSelectionsList.length - 1; i++)  //-1 to skip the incremental ids
        {
            let identifier;
            if (i == 0)
                identifier = 'cat';
            else if (i == 1)
                identifier = 'type';
            else if (i == 2)
                identifier = 'area';
            else
                console.error('Error: unknown identifier');
            a.href += identifier + '=';

            for (let j = 0; j < userviewSelectionsList[i].length; j++) {
                let symbol = '+';
                if (j == userviewSelectionsList[i].length - 1) {
                    symbol = '&';
                    if (i == userviewSelectionsList.length - 2) symbol = '';
                }
                a.href += userviewSelectionsList[i][j] + symbol;
            }
        } //Example result: UserView.html?cat=MSG+MSG_RSS+MSG_IODC&type=ARMRGB+FOGRGB+HRVCHN&area=FDK+EU+GR

        document.body.appendChild(a);
        a.click();
        a.remove();
    })



    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });

})()
