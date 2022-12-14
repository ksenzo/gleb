//let tg = window.Telegram.WebApp;
let userId = 307938801;
//let userName = `${tg.initDataUnsafe.user.username}`;
let balance = null
$(document).ready(() => {
     // tg.expand();
     // tg.MainButton.text = "Депозит";
     // tg.MainButton.show();
    let keysAll = [...document.querySelectorAll('.key')];
    $('#keys').show();
    $('.user_hat_body').text('user_name')

    $.ajax({
        url: '/server/ajax_check_user',
        data: {'telegram_id': userId},
        success: (result) => {
            console.log(result)
            if (result.message === 'account_exists') {
                $('#balance').text(`${result.balance} UAH`)
                $('.bonus_progress').css('width', `${(result.bonus_game_count) * 11.7}px`);
                for (let i = 0; i <= result.keys - 1; i++) {
                    keysAll[i].classList.add('__active');
                }
                balance = parseInt(result.balance)
                if (result.balance >= result.last_bet) {
                    $('#bet_amount').val(result.last_bet)
                } else if (result.balance < result.last_bet) {
                    $('#bet_amount').val(result.balance)
                }
                if ((result.bonus_game_count === 0 && result.keys > 0)) {
                    bonusGameStart();
                } else {
                    $('#bonus_counter').text(`${result.bonus_game_count}/12`);
                }
            } else if (result.message === 'no_account') {
                $('#balance').text('no_account')
            }
        },
        async: false
    })
    //tg.MainButton.onClick(showDeposit)
})

let theme = localStorage.getItem('data-theme');
let darkT = 'url(/static/img/dark.gif)';
let lightT = 'url(/static/img/light.gif)';

if (theme) {

    $('#select_chests').css('background-image', theme);
    $('#bonus_game_start').css('background-image', theme);
} else {
    localStorage.setItem('data-theme', darkT);
    let theme = localStorage.getItem('data-theme');
    $('#select_chests').css('background-image', theme);
    $('#bonus_game_start').css('background-image', theme);
}



$(document).on("click", ".settings_theme_btn_turner", function () {
    let oldTheme = localStorage.getItem('data-theme');
    if (oldTheme == darkT) {
        localStorage.setItem('data-theme', lightT);
        let newTheme = localStorage.getItem('data-theme');
        $('#select_chests').css('background-image', newTheme);
        $('#bonus_game_start').css('background-image', newTheme);
        theme = lightT;
    } else if (oldTheme == lightT) {
        localStorage.setItem('data-theme', darkT);
        let newTheme = localStorage.getItem('data-theme');
        $('#select_chests').css('background-image', newTheme);
        $('#bonus_game_start').css('background-image', newTheme);
        theme = darkT;
    }
});

function bonusGameStart() {
    $("#game_to_start").hide();
    $('.key').removeClass('__active');
    $('#keys').hide();
    $("#bonus_game_start").show();
    $('.bonus_row_bonus_game').addClass('__active');
    $('.bonus_img img').attr('src', '/static/img/open_bonus.svg');
    $('.bonus_img').addClass('__active');
    $('.bonus_img2').addClass('__active');
    $('.bonus_counter').addClass('__active');
    $.ajax({
        url: '/server/ajax_bonus_game',
        data: {'telegram_id': userId},
        success: (result) => {
            if (result.message === 'bonus_game_active') {
                let keys = [...document.querySelectorAll('.key2')];
                for (let i = 0; i < result.keys; i++) {
                    keys[i].classList.add('__active');
                }
                $('#bonus_chest_1').attr("onclick", "selectBonusChest('left-1')")
                $('#bonus_chest_2').attr("onclick", "selectBonusChest('center-1')")
                $('#bonus_chest_3').attr("onclick", "selectBonusChest('right-1')")
                $('#bonus_chest_4').attr("onclick", "selectBonusChest('left-2')")
                $('#bonus_chest_5').attr("onclick", "selectBonusChest('center-2')")
                $('#bonus_chest_6').attr("onclick", "selectBonusChest('right-2')")
            }
        }
    })
}


function keysNull() {
    $.ajax({
        url: '/server/key_null_throw',
        data: {'telegram_id': userId},
        success: () => {
            window.location.reload();
        }
    });
}

let bonusTotal = 0;
$('.bonus_total_text').text(`total: ${bonusTotal} UAH`);

function selectBonusChest(choice) {
    $('.bonus_sunduk').attr("onclick", "");

        if (choice === 'left-1') {
            $('#bonus_chest_1').attr("onclick", "");
        } else if (choice === 'center-1') {
            $('#bonus_chest_2').attr("onclick", "");
        } else if (choice === 'right-1') {
            $('#bonus_chest_3').attr("onclick", "");
        } else if (choice === 'left-2') {
            $('#bonus_chest_4').attr("onclick", "");
        } else if (choice === 'center-2') {
            $('#bonus_chest_5').attr("onclick", "");
        } else if (choice === 'right-2') {
            $('#bonus_chest_6').attr("onclick", "");
        }

        $("#game_to_start").hide();
        $("#bonus_game_start").show();
        $.ajax({
            url: '/server/ajax_start_bonus_game',
            data: {'telegram_id': userId},
            success: (result) => {
                let sunduki = [...document.querySelectorAll('.bonus_sunduk')];
                let resultsOfBonus = [...document.querySelectorAll('.bonus_game_result')];
                let chestOpenedWin = sunduki[0].getAttribute("data-original-win");
                let chestOpenedLose = sunduki[0].getAttribute("data-original-lose");
                let keys = [...document.querySelectorAll('.key2')];

                bonusTotal += result.winning;

                keys[result.keys].classList.remove('__active');
                $('.bonus_total_text').text(`total: ${bonusTotal} UAH`);

                let winBonus = (sunduk, bonus) => {
                    let chance = (result.winning / result.avarage);

                    sunduk.setAttribute('src', chestOpenedWin);
                    setTimeout(() => {
                        bonus.append(`${result.winning} UAH X${chance}`);
                    }, 1000);
                    sunduk.classList.add('__active');
                    if (chance == 10 || chance == 1.5) {
                        bonus.classList.add('__green');
                    } else if (chance == 0.01 || chance == 0.5) {
                        bonus.classList.add('__red');
                    } else if (chance == 1) {
                        bonus.classList.add('__yellow');
                    }
                }

                if (result.keys != 0) {
                    if (choice === 'left-1') {
                        winBonus(sunduki[0], resultsOfBonus[0]);
                        setTimeout(() => {
                            sunduki[0].setAttribute('src', '/static/img/open_bonus_case.png')
                        }, 1000);
                    } else if (choice === 'center-1') {
                        winBonus(sunduki[1], resultsOfBonus[1]);
                        setTimeout(() => {
                            sunduki[1].setAttribute('src', '/static/img/open_bonus_case.png')
                        }, 1000);
                    } else if (choice === 'right-1') {
                        winBonus(sunduki[2], resultsOfBonus[2]);
                        setTimeout(() => {
                            sunduki[2].setAttribute('src', '/static/img/open_bonus_case.png')
                        }, 1000);
                    } else if (choice === 'left-2') {
                        winBonus(sunduki[3], resultsOfBonus[3]);
                        setTimeout(() => {
                            sunduki[3].setAttribute('src', '/static/img/open_bonus_case.png')
                        }, 1000);
                    } else if (choice === 'center-2') {
                        winBonus(sunduki[4], resultsOfBonus[4]);
                        setTimeout(() => {
                            sunduki[4].setAttribute('src', '/static/img/open_bonus_case.png')
                        }, 1000);
                    } else if (choice === 'right-2') {
                        winBonus(sunduki[5], resultsOfBonus[5]);
                        setTimeout(() => {
                            sunduki[5].setAttribute('src', '/static/img/open_bonus_case.png')
                        }, 1000);
                    }
                } else if (result.keys == 0) {
                    if (choice === 'left-1') {
                        winBonus(sunduki[0], resultsOfBonus[0]);
                        setTimeout(() => {
                            sunduki[0].setAttribute('src', '/static/img/open_bonus_case.png')
                        }, 1000);
                    } else if (choice === 'center-1') {
                        winBonus(sunduki[1], resultsOfBonus[1]);
                        setTimeout(() => {
                            sunduki[1].setAttribute('src', '/static/img/open_bonus_case.png')
                        }, 1000);
                    } else if (choice === 'right-1') {
                        winBonus(sunduki[2], resultsOfBonus[2]);
                        setTimeout(() => {
                            sunduki[2].setAttribute('src', '/static/img/open_bonus_case.png')
                        }, 1000);
                    } else if (choice === 'left-2') {
                        winBonus(sunduki[3], resultsOfBonus[3]);
                        setTimeout(() => {
                            sunduki[3].setAttribute('src', '/static/img/open_bonus_case.png')
                        }, 1000);
                    } else if (choice === 'center-2') {
                        winBonus(sunduki[4], resultsOfBonus[4]);
                        setTimeout(() => {
                            sunduki[4].setAttribute('src', '/static/img/open_bonus_case.png')
                        }, 1000);
                    } else if (choice === 'right-2') {
                        winBonus(sunduki[5], resultsOfBonus[5]);
                        setTimeout(() => {
                            sunduki[5].setAttribute('src', '/static/img/open_bonus_case.png')
                        }, 1000);
                    }
                    let newGameButton = `<div style="display: flex; align-items: center; justify-content: center; width: 100%;"><button class="button_new_game btn_start_game btn_new_game_bonus" onclick="keysNull()">Новая игра</button></div>`
                    setTimeout(() => {
                        $("#bonus_game_start").append(newGameButton)
                    }, 1000);
                    $('.bonus_chest').addClass('__active');
                }  else {
                    console.log('error')
                }
                $('#bonus_chest_1').attr("onclick", "selectBonusChest('left-1')")
                $('#bonus_chest_2').attr("onclick", "selectBonusChest('center-1')")
                $('#bonus_chest_3').attr("onclick", "selectBonusChest('right-1')")
                $('#bonus_chest_4').attr("onclick", "selectBonusChest('left-2')")
                $('#bonus_chest_5').attr("onclick", "selectBonusChest('center-2')")
                $('#bonus_chest_6').attr("onclick", "selectBonusChest('right-2')")
            }
        })
}


//bonusGameStart();
//selectBonusChest('left');


function showDeposit(){
    $("#game_to_start").hide();
    $("#deposit_container").show()
    // tg.MainButton.text = "Играть";
    // tg.BackButton.show()
    // tg.BackButton.onClick(showGame)
}

function showGame(){
    $("#deposit_container").hide()
    $("#game_to_start").show();
     //tg.BackButton.hide()
}

let amount = document.getElementById('bet_amount')
function handleMinus() {
    if (amount.value <= 5) {
        amount.value -= 0
    } else if (amount.value <= 50) {
        amount.value -= 5
    } else if (50 < amount.value && amount.value <= 100) {
        amount.value -= 10
    } else if (100 < amount.value && amount.value <= 500) {
        amount.value -= 50
    } else if (500 < amount.value && amount.value <= 1000) {
        amount.value -= 100
    } else if (1000 < amount.value && amount.value <= 5000) {
        amount.value -= 500
    } else if (5000 < amount.value && amount.value <= 10000) {
        amount.value -= 1000
    }
}

function handlePlus() {
    if (amount.value < 50) {
        if (parseInt(amount.value) + 5 <= balance) {
            amount.value = parseInt(amount.value) + 5
        } else {
            amount.value = balance
        }
    } else if (50 <= amount.value && amount.value < 100) {
        if (parseInt(amount.value) + 10 <= balance) {
            amount.value = parseInt(amount.value) + 10
        } else {
            amount.value = balance
        }
    } else if (100 <= amount.value && amount.value < 500) {
        if (parseInt(amount.value) + 50 <= balance) {
            amount.value = parseInt(amount.value) + 50
        } else {
            amount.value = balance
        }
    } else if (500 <= amount.value && amount.value < 1000) {
        if (parseInt(amount.value) + 100 <= balance) {
            amount.value = parseInt(amount.value) + 100
        } else {
            amount.value = balance
        }
    } else if (1000 <= amount.value && amount.value < 5000) {
        if (parseInt(amount.value) + 500 <= balance) {
            amount.value = parseInt(amount.value) + 500
        } else {
            amount.value = balance
        }
    } else if (5000 <= amount.value && amount.value < 10000) {
        if (parseInt(amount.value) + 1000 <= balance) {
            amount.value = parseInt(amount.value) + 1000
        } else {
            amount.value = balance
        }
    }
}

function setAmount(bet_amount) {
    if (bet_amount <= balance) {
        amount.value = bet_amount
    } else {
        amount.value = balance
    }
}

function doubleBet() {
    if (amount.value * 2 <= balance){
        if (amount.value <= 5000) {
            amount.value = amount.value * 2
        } else {
            amount.value = 10000
        }
    } else {
        amount.value = balance
    }
}

function startGame() {
    $('.btn_start_game').attr('onclick', '');
    $.ajax({
        url: '/server/ajax_check_bet_amount',
        data: {'telegram_id': userId, 'bet_amount': amount.value},
        success: (result) => {
            if (result.message === 'bet_amount_ok') {

                $.ajax({
                    url: '/server/ajax_start_game',
                    data: {'telegram_id': userId, 'bet_amount': amount.value},
                    success: (result) => {
                        if (result.message === 'game_starts') {
                            $('#balance').text(`${result.balance} UAH`)
                            $("#chest_1").attr("class", "chest");
                            $("#chest_2").attr("class", "chest");
                            $("#chose_bet_size").hide();
                            $('.select_chests').addClass('__active-game');
                            $('.chest').addClass('__active');
                            $('.sunduki').addClass('__active');
                            $('#select_chest').append(
                                `<div class="new_game_render_wrap">
                                        <div class="choose_sunduk">ВЫБЕРИТЕ СУНДУК</div>
                                        <img class="diamond" id="d1" src="/static/img/d1.png">
                                        <img class="diamond" id="d2" src="/static/img/d2.png">
                                        <img class="diamond" id="d3" src="/static/img/d3.png">
                                        <img class="diamond" id="d4" src="/static/img/d4.png">
                                        <img class="diamond" id="d5" src="/static/img/d5.png">
                                        <img class="diamond" id="d6" src="/static/img/d6.png">
                                        <img class="diamond" id="d7" src="/static/img/d7.png">
                                        <img class="diamond" id="d8" src="/static/img/d8.png">
                                        <img class="diamond" id="d9" src="/static/img/d9.png">
                                        <img class="diamond" id="d10" src="/static/img/d3.png">
                                    </div>`
                            )
                            $(".chest_1").addClass('active_game_chest1');
                            $(".chest_2").addClass('active_game_chest2');
                        }
                    }
                })
            } else if (result.message === 'not_enough_balance') {
                $('.not_money').addClass('__active');
            }
        }
    })
}




function selectChest(choice) {
    $.ajax({
        url: '/server/ajax_select_chest',
        data: {'telegram_id': userId, 'choice': choice},
        success: (result) => {
            if (result.message === 'chest_selected') {
                setTimeout(function(){
                    $('#select_chest').empty();
                }, 501);
                $('#balance').text(`${result.balance} UAH`);
                let firstChest = document.querySelector('#chest_1')
                let secondChest = document.querySelector('#chest_2')
                let firstChestOpenedWin = firstChest.getAttribute("data-original-win")
                let secondChestOpenedWin = secondChest.getAttribute("data-original-win")
                let firstChestOpenedLose = firstChest.getAttribute("data-original-lose")
                let secondChestOpenedLose = secondChest.getAttribute("data-original-lose")
                let keys = [...document.querySelectorAll('.key')];

                if (result.key_result === 'key_winning') {
                    setTimeout(() => {keys[result.keys - 1].classList.add('__active'); $('.bonus_counter').addClass('__active')}, 1500);
                    if (choice === 'left') {
                        setTimeout(function(){
                            firstChest.insertAdjacentHTML('beforebegin','<div class="key_win_left"></div>');
                        }, 500);
                    } else if (choice === 'right') {
                        setTimeout(function(){
                            secondChest.insertAdjacentHTML('beforebegin','<div class="key_win_right"></div>');
                        }, 500);
                    }
                }

                if (result.winning === 'game_winning') {
                    setTimeout(function(){
                        $("#game_result").append(
                            `<div>
                                <div class="win_msg_wrap">
                                    <span class="win_font">ПОБЕДА!</span>
                                    <span class="win_font">${result.winning_amount} UAH</span>
                                </div>
                            </div>`
                        )
                    }, 500);
                    if (choice === 'left') {
                        firstChest.setAttribute('src', firstChestOpenedWin);
                        secondChest.setAttribute('src', secondChestOpenedLose);
                        $('.sunduk').addClass('__not_active');
                        $('.sunduk2').addClass('__not_active');
                    } else if (choice === 'right') {
                        secondChest.setAttribute('src', secondChestOpenedWin);
                        $('.sunduk').addClass('__not_active');
                        $('.sunduk2').addClass('__not_active');
                        firstChest.setAttribute('src', firstChestOpenedLose);
                    }
                } else if (result.winning === 'game_loosing') {
                    setTimeout(function(){
                        $("#game_result").append(
                            `<div style="display: flex; flex-direction: column; align-items: center;">
                                <div class="win_msg_wrap">
                                    <span class="win_font">ПОПРОБУЙ ЕЩЕ РАЗ!</span>    
                                </div>
                            </div>`
                        )
                    }, 500);

                    if (choice === 'left') {
                        firstChest.setAttribute('src', firstChestOpenedLose);
                        $('.sunduk').addClass('__not_active');
                        $('.sunduk2').addClass('__not_active');
                        secondChest.setAttribute('src', secondChestOpenedWin);
                    } else if (choice === 'right') {
                        secondChest.setAttribute('src', secondChestOpenedLose);
                        $('.sunduk').addClass('__not_active');
                        $('.sunduk2').addClass('__not_active');
                        firstChest.setAttribute('src', firstChestOpenedWin);
                    }
                }

                $('#chest_1').attr("onclick", "")
                $('#chest_2').attr("onclick", "")
                var newGameButton = `<div class="new_game_render_wrap">
                                        <button class="button_new_game btn_start_game" onclick="window.location.reload();">ИГРАТЬ</button>
                                        <img class="diamond" id="d1" src="/static/img/d1.png">
                                        <img class="diamond" id="d2" src="/static/img/d2.png">
                                        <img class="diamond" id="d3" src="/static/img/d3.png">
                                        <img class="diamond" id="d4" src="/static/img/d4.png">
                                        <img class="diamond" id="d5" src="/static/img/d5.png">
                                        <img class="diamond" id="d6" src="/static/img/d6.png">
                                        <img class="diamond" id="d7" src="/static/img/d7.png">
                                        <img class="diamond" id="d8" src="/static/img/d8.png">
                                        <img class="diamond" id="d9" src="/static/img/d9.png">
                                        <img class="diamond" id="d10" src="/static/img/d3.png">
                                    </div>`
                // let repeatOnclick = `repeatBetGame(${winning_amount / 2});`
                // var repeatBetButton = `<button id="repeatBetButton" class="button_new_game">Повторить<br>ставку</button>`
                setTimeout(function(){
                    $("#game_to_start").append(newGameButton);
                }, 500);

                // repeat_button = document.getElementById('repeatBetButton')
                // repeat_button.onclick =
                // repeat_button.addEventListener("click", repeatBetGame(winning_amount / 2));
            }
        }
    })
}

let flag = true;

$(document).on("click", ".active_game_chest1", function () {
    if (flag === true) {
        flag = false;
        selectChest('left');
    }
})

$(document).on("click", ".active_game_chest2", function () {
    if (flag === true) {
        flag = false;
        selectChest('right');
    }
});

function repeatBetGame(amount) {
    $.ajax({
        url: '/server/ajax_check_bet_amount',
        data: {'telegram_id': userId, 'bet_amount': amount},
        success: (result) => {
            if (result.message === 'bet_amount_ok') {
                // firstChest = document.querySelector('#chest_1')
                // secondChest = document.querySelector('#chest_2')
                $.ajax({
                    url: '/server/ajax_start_game',
                    data: {'telegram_id': userId, 'bet_amount': amount},
                    success: (result) => {
                        if (result.message === 'game_starts') {
                            $('#balance').text(`${result.balance} UAH`)
                            $("#chest_1").attr("class", "chest");
                            $("#chest_2").attr("class", "chest");
                            $("#chose_bet_size").hide();
                            $('#select_chest').text('Выберите сундук')
                        }
                    }
                })
            }
        }
    })
}


let deposit_amount = document.getElementById('deposit_amount')
function handleMinusDep() {
    if (deposit_amount.value <= 50) {
        deposit_amount.value -= 0
    } else if (50 < deposit_amount.value && deposit_amount.value <= 100) {
        deposit_amount.value -= 10
    } else if (100 < deposit_amount.value && deposit_amount.value <= 500) {
        deposit_amount.value -= 50
    } else if (500 < deposit_amount.value && deposit_amount.value <= 1000) {
        deposit_amount.value -= 100
    } else if (1000 < deposit_amount.value && deposit_amount.value <= 5000) {
        deposit_amount.value -= 500
    } else if (5000 < deposit_amount.value && deposit_amount.value <= 10000) {
        deposit_amount.value -= 1000
    } else if (10000 < deposit_amount.value && deposit_amount.value <= 30000) {
        deposit_amount.value -= 5000
    }
}

function handlePlusDep() {
    if (50 <= deposit_amount.value && deposit_amount.value < 100) {
        deposit_amount.value = parseInt(deposit_amount.value) + 10
    } else if (100 <= deposit_amount.value && deposit_amount.value < 500) {
        deposit_amount.value = parseInt(deposit_amount.value) + 50
    } else if (500 <= deposit_amount.value && deposit_amount.value < 1000) {
        deposit_amount.value = parseInt(deposit_amount.value) + 100
    } else if (1000 <= deposit_amount.value && deposit_amount.value < 5000) {
        deposit_amount.value = parseInt(deposit_amount.value) + 500
    } else if (5000 <= deposit_amount.value && deposit_amount.value < 10000) {
        deposit_amount.value = parseInt(deposit_amount.value) + 1000
    } else if (10000 <= deposit_amount.value && deposit_amount.value < 30000) {
        deposit_amount.value = parseInt(deposit_amount.value) + 5000
    }
}

function setAmountDep(deposit_amount_value) {
    deposit_amount.value = deposit_amount_value
}

let openSetting = $('#settings_btn');
let settingsBlock = $('.settings');

$(document).on("click", "#settings_btn", function () {
    settingsBlock.addClass('__active');
    openSetting.addClass('__active');
    $('body').addClass('__noscroll');
});

$(document).on("click", ".close_msg", function () {
    $('.not_money').removeClass('__active');
});

$(document).on("click", ".settings_close", function () {
    settingsBlock.removeClass('__active');
    openSetting.removeClass('__active');
    $('body').removeClass('__noscroll');
});

$(document).on("click", ".settings_theme_btn_turner", function () {
    $(this).toggleClass('__active');
    $(this).children().eq(1).toggleClass('__active');
});

const buttonDoubleBet = document.querySelector('.button_double_bet');
const buttonMinus = document.querySelector('.button_minus');
const buttonPlus = document.querySelector('.button_plus');
const btnStartGame = document.querySelector('.btn_start_game');

function clickAnim(e) {
    e.classList.add('clicked');
    setTimeout(()=> {
        e.classList.remove('clicked')
    },300);
}

$(document).on("click", ".button_double_bet", function () {
    clickAnim(buttonDoubleBet);
});

$(document).on("click", ".button_minus", function () {
    clickAnim(buttonMinus);
});

$(document).on("click", ".button_plus", function () {
    clickAnim(buttonPlus);
});

$(document).on("click", ".btn_start_game", function () {
    clickAnim(btnStartGame);
});