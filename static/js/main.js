let tg = window.Telegram.WebApp;
let userId = `${tg.initDataUnsafe.user.id}`;
let balance = null
$(document).ready(() => {
    tg.expand();
    tg.MainButton.text = "Депозит";
    tg.MainButton.show();

    $.ajax({
        url: '/server/ajax_check_user',
        data: {'telegram_id': userId},
        success: (result) => {
            if (result.message === 'account_exists') {
                $('#balance').text(`${result.balance} UAH`)
                balance = parseInt(result.balance)
                if (result.balance >= result.last_bet) {
                    $('#bet_amount').val(result.last_bet)
                } else if (result.balance < result.last_bet) {
                    $('#bet_amount').val(result.balance)
                }
                if (result.bonus_game_count === 0) {
                    bonusGameStart()
                } else {
                    $('#bonus_counter').text(`${result.bonus_game_count}/12`);
                }
            } else if (result.message === 'no_account') {
                $('#balance').text('no_account')
            }
        },
        async: false
    })
    tg.MainButton.onClick(showDeposit)
})

function bonusGameStart(){
    $("#game_to_start").hide();
    $("#bonus_game_start").show()
    $.ajax({
        url: '/server/ajax_bonus_game',
        data: {'telegram_id': userId},
        success: (result) => {
            if (result.message === 'bonus_game_active') {
                $('#bonus_chest_1').attr("onclick", "selectBonusChest('left')")
                $('#bonus_chest_2').attr("onclick", "selectBonusChest('center')")
                $('#bonus_chest_3').attr("onclick", "selectBonusChest('right')")
            }
        }
    })
}

function selectBonusChest(choice){
    $.ajax({
        url: '/server/ajax_start_bonus_game',
        data: {'telegram_id': userId},
        success: (result) => {
            let firstChest = document.querySelector('#bonus_chest_1')
            let secondChest = document.querySelector('#bonus_chest_2')
            let thirdChest = document.querySelector('#bonus_chest_3')

            let firstChestOpened = firstChest.getAttribute("data-original")
            let secondChestOpened = secondChest.getAttribute("data-original")
            let thirdChestOpened = thirdChest.getAttribute("data-original")

            firstChest.setAttribute('src', firstChestOpened)
            secondChest.setAttribute('src', secondChestOpened)
            thirdChest.setAttribute('src', secondChestOpened)
            if (choice === 'left') {
                $("#bonus_game_result_left").text(result.winning)
                $("#bonus_game_result_center").text(result.chest_2)
                $("#bonus_game_result_right").text(result.chest_3)
            } else if (choice === 'center') {
                $("#bonus_game_result_center").text(result.winning)
                $("#bonus_game_result_left").text(result.chest_2)
                $("#bonus_game_result_right").text(result.chest_3)
            } else if (choice === 'right') {
                $("#bonus_game_result_right").text(result.winning)
                $("#bonus_game_result_left").text(result.chest_2)
                $("#bonus_game_result_center").text(result.chest_3)
            }
            $('#bonus_chest_1').attr("onclick", "")
            $('#bonus_chest_2').attr("onclick", "")
            $('#bonus_chest_3').attr("onclick", "")
            var newGameButton = `<button class="button_new_game" onclick="window.location.reload();">Новая игра</button>`
            $("#bonus_game_start").append(newGameButton);
        }
    })
}

function showDeposit(){
    $("#game_to_start").hide();
    $("#deposit_container").show()
    tg.MainButton.text = "Играть";
    tg.BackButton.show()
    tg.BackButton.onClick(showGame)
}

function showGame(){
    $("#deposit_container").hide()
    $("#game_to_start").show();
    tg.BackButton.hide()
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
    $.ajax({
        url: '/server/ajax_check_bet_amount',
        data: {'telegram_id': userId, 'bet_amount': amount.value},
        success: (result) => {
            if (result.message === 'bet_amount_ok') {
                // firstChest = document.querySelector('#chest_1')
                // secondChest = document.querySelector('#chest_2')
                $.ajax({
                    url: '/server/ajax_start_game',
                    data: {'telegram_id': userId, 'bet_amount': amount.value},
                    success: (result) => {
                        if (result.message === 'game_starts') {
                            $('#balance').text(`${result.balance} UAH`)
                            $("#chest_1").attr("class", "chest");
                            $("#chest_2").attr("class", "chest");
                            $("#chose_bet_size").hide();
                                $('#select_chest').append(
                                    `<div class="new_game_render_wrap">
                                        <div class="choose_sunduk">ВЫБЕРИТЕ СУНДУК</div>
                                    </div>`
                                )
                            $('#chest_1').attr("onclick", "selectChest('left')")
                            $('#chest_2').attr("onclick", "selectChest('right')")
                        }
                    }
                })
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
                $('#balance').text(`${result.balance} UAH`)
                let firstChest = document.querySelector('#chest_1')
                let secondChest = document.querySelector('#chest_2')
                let firstChestOpenedWin = firstChest.getAttribute("data-original-win")
                let secondChestOpenedWin = secondChest.getAttribute("data-original-win")
                let firstChestOpenedLose = firstChest.getAttribute("data-original-lose")
                let secondChestOpenedLose = secondChest.getAttribute("data-original-lose")

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

//selectChest('left');

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
                            $('#chest_1').attr("onclick", "selectChest('left')")
                            $('#chest_2').attr("onclick", "selectChest('right')")
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