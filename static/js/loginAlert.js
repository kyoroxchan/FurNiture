function clickEvent() {
    var res = confirm("ログインしてください");
    if( res == true ) {
        // OKなら移動
        window.location.href = "http://localhost:5000/login";
    }
}