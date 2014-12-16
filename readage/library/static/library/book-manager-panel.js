var cq;

/* 
 * remember to write load code here
 */

$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
	console.log(e.target);
	cq = e.target;
	console.log(e.relatedTarget);
});



$( document ).ready(function() { 
	/*
    $('#magic').hover(
        function(){
            $(document).find('#usertable').slideDown(250); //.fadeIn(250)
			$('#userborrow').addClass("panelloding");
			setTimeout(function(){
			  $('#userborrow').removeClass("panelloding");
			}, 2000);
        },
        function(){
			setTimeout(function(){
				  $(document).find('#usertable').slideUp(250); //.fadeOut(205)
			}, 3000);
        }
    );
	*/

    csrftoken = getCookie('csrftoken');

    $('#magic').click(function(){
    	csrftoken = getCookie('csrftoken');

    	var curl = $('#find-user-url').val();
    	var search = $('#find-user-input').val();

    	$('#find-user-tbody').load(curl+search, function(){
    		$('.choose-user').click(function(){
				var uid = $(this).attr('userid');
				var uname = $(this).attr('username');
				$('#display-username').html(uname);
				$('#borrow-book-uid').val(uid);
				$('#find-user-tbody').html('');
				$('#borrow-book-tbody').html('');
				$('#borrow-book-bid').focus();
				return false;
			});
    	});
    	return false;
    });

    

    $('#magic-borrow').click(function(){
    	var curl = $('#borrow-book-url').val();
    	var uid = $('#borrow-book-uid').val();
    	var bid = $('#borrow-book-bid').val();

    	if(!bid){
    		alert('empty book id!');
    		return false;
    	}

    	csrftoken = getCookie('csrftoken');
    	$.post(
    		'/borrow/' + bid + '/u' + uid + '/',
    		{'csrfmiddlewaretoken':csrftoken},
    		function(data){
    			var obj = $.parseJSON(data);
    			var txt = null;
				if(obj.status == 'Error'){
					txt = '<tr><td><div class="alert alert-danger"><strong>Error!</strong> ' 
							+ 'err: <strong>' + obj.err 
							+ '</strong> msg: <strong>' + obj.message
							+ '</strong> uid: <strong>' + uid 
							+ '</strong> bid: <strong>' + bid
							+ '</strong></div></td></tr>';
				} else if(obj.status == 'OK'){
					txt = '<tr><td><div class="alert alert-success">' 
							+ '<strong>借出成功！'
							+ '</strong> uid: <strong>' + uid 
							+ '</strong> bid: <strong>' + bid
							+ '</strong></div></td></tr>';
				}
				$('#borrow-book-tbody').append(txt);
				$('#borrow-book-bid').val('');
    		}
    	);
    });

	// return book
	$('#magic-return').click(function(){
		var bid = $('#return-book-bid').val();

    	if(!bid){
    		alert('empty book id!');
    		return false;
    	}

    	csrftoken = getCookie('csrftoken');
    	$.post(
    		'/return/' + bid + '/',
    		{'csrfmiddlewaretoken':csrftoken},
    		function(data){
    			var obj = $.parseJSON(data);
    			var txt = null;
				if(obj.status == 'Error'){
					txt = '<tr><td><div class="alert alert-danger"><strong>Error!</strong> ' 
							+ 'err: <strong>' + obj.err 
							+ '</strong> msg: <strong>' + obj.message
							+ '</strong> bid: <strong>' + bid
							+ '</strong></div></td></tr>';
				} else if(obj.status == 'OK'){
					txt = '<tr><td><div class="alert alert-success">' 
							+ '<strong>还书成功！'
							+ '</strong> bid: <strong>' + bid
							+ '</strong></div></td></tr>';
					$('#return-book-num').text(parseInt($('#return-book-num').text())+1);
				}
				$('#return-tbody').append(txt);
				$('#return-book-bid').val('');
    		}
    	);
	});

	/*
	 * booking book
	 */
	$('#magic2').click(function(){
    	csrftoken = getCookie('csrftoken');

    	var curl = $('#find-user-url2').val();
    	var search = $('#find-user-input2').val();

    	$('#find-user-tbody2').load(curl+search, function(){
    		$('.choose-user').click(function(){
				var uid = $(this).attr('userid');
				var uname = $(this).attr('username');
				$('#display-username2').html(uname);
				$('#borrow-book-uid2').val(uid);
				$('#find-user-tbody2').html('');
				$('#borrow-book-tbody2').html('');
				$('#borrow-book-bid2').focus();
				return false;
			});
    	});
    	return false;
    });



    $('#magic-borrow2').click(function(){
    	var curl = $('#borrow-book-url2').val();
    	var uid = $('#borrow-book-uid2').val();
    	var bid = $('#borrow-book-bid2').val();

    	if(!bid){
    		alert('empty book id!');
    		return false;
    	}

    	csrftoken = getCookie('csrftoken');
    	$.post(
    		'/next/' + bid + '/u' + uid + '/',
    		{'csrfmiddlewaretoken':csrftoken},
    		function(data){
    			var obj = $.parseJSON(data);
    			var txt = null;
				if(obj.status == 'Error'){
					txt = '<tr><td><div class="alert alert-danger"><strong>Error!</strong> ' 
							+ 'err: <strong>' + obj.err 
							+ '</strong> msg: <strong>' + obj.message
							+ '</strong> uid: <strong>' + uid 
							+ '</strong> bid: <strong>' + bid
							+ '</strong></div></td></tr>';
				} else if(obj.status == 'OK'){
					txt = '<tr><td><div class="alert alert-success">' 
							+ '<strong>预约取书成功！'
							+ '</strong> uid: <strong>' + uid 
							+ '</strong> bid: <strong>' + bid
							+ '</strong></div></td></tr>';
				}
				$('#borrow-book-tbody2').append(txt);
				$('#borrow-book-bid2').val('');
    		}
    	);
    });

	// return to shelf
	$('#magic-return2').click(function(){
		var bid = $('#return-book-bid2').val();

    	if(!bid){
    		alert('empty book id!');
    		return false;
    	}

    	csrftoken = getCookie('csrftoken');
    	$.post(
    		'/readify/' + bid + '/',
    		{'csrfmiddlewaretoken':csrftoken},
    		function(data){
    			var obj = $.parseJSON(data);
    			var txt = null;
				if(obj.status == 'Error'){
					txt = '<tr><td><div class="alert alert-danger"><strong>Error!</strong> ' 
							+ 'err: <strong>' + obj.err 
							+ '</strong> msg: <strong>' + obj.message
							+ '</strong> bid: <strong>' + bid
							+ '</strong></div></td></tr>';
				} else if(obj.status == 'OK'){
					txt = '<tr><td><div class="alert alert-success">' 
							+ '<strong>图书整理上架成功！'
							+ '</strong> bid: <strong>' + bid
							+ '</strong></div></td></tr>';
					$('#return-book-shelf-num').text(parseInt($('#return-book-shelf-num').text())+1);

				}
				$('#return-tbody2').append(txt);
				$('#return-book-bid2').val('');
    		}
    	);
	});

	// move out of shelf

	$('#magic-return3').click(function(){
		var bid = $('#return-book-bid3').val();

    	if(!bid){
    		alert('empty book id!');
    		return false;
    	}

    	csrftoken = getCookie('csrftoken');
    	$.post(
    		'/disappear/' + bid + '/',
    		{'csrfmiddlewaretoken':csrftoken},
    		function(data){
    			var obj = $.parseJSON(data);
    			var txt = null;
				if(obj.status == 'Error'){
					txt = '<tr><td><div class="alert alert-danger"><strong>Error!</strong> ' 
							+ 'err: <strong>' + obj.err 
							+ '</strong> msg: <strong>' + obj.message
							+ '</strong> bid: <strong>' + bid
							+ '</strong></div></td></tr>';
				} else if(obj.status == 'OK'){
					txt = '<tr><td><div class="alert alert-success">' 
							+ '<strong>图书丢失下架成功！'
							+ '</strong> bid: <strong>' + bid
							+ '</strong></div></td></tr>';
					$('#del-book-num').text(parseInt($('#del-book-num').text())+1);
				}
				$('#return-tbody3').append(txt);
				$('#return-book-bid3').val('');
    		}
    	);
	});

	// realize enter
	// borrow
	$('#find-user-input').bind("enterKey",function(e){
		//do stuff here
		$('#magic').click();
	});

	$('#find-user-input').keyup(function(e){
		if(e.keyCode == 13){
			$(this).trigger("enterKey");
		}
	});

	$('#borrow-book-bid').bind("enterKey",function(e){
		//do stuff here
		$('#magic-borrow').click();
	});

	$('#borrow-book-bid').keyup(function(e){
		if(e.keyCode == 13){
			$(this).trigger("enterKey");
		}
	});

	// return book
	$('#return-book-bid').bind("enterKey",function(e){
		//do stuff here
		$('#magic-return').click();
	});

	$('#return-book-bid').keyup(function(e){
		if(e.keyCode == 13){
			$(this).trigger("enterKey");
		}
	});

	// ording book
	$('#borrow-book-bid2').bind("enterKey",function(e){
		//do stuff here
		$('#magic-borrow2').click();
	});

	$('#borrow-book-bid2').keyup(function(e){
		if(e.keyCode == 13){
			$(this).trigger("enterKey");
		}
	});

	$('#find-user-input2').bind("enterKey",function(e){
		//do stuff here
		$('#magic2').click();
	});

	$('#find-user-input2').keyup(function(e){
		if(e.keyCode == 13){
			$(this).trigger("enterKey");
		}
	});

	// get book to shelf
	$('#return-book-bid2').bind("enterKey",function(e){
		//do stuff here
		$('#magic-return2').click();
	});

	$('#return-book-bid2').keyup(function(e){
		if(e.keyCode == 13){
			$(this).trigger("enterKey");
		}
	});

	// lose the book
	$('#return-book-bid3').bind("enterKey",function(e){
		//do stuff here
		$('#magic-return3').click();
	});

	$('#return-book-bid3').keyup(function(e){
		if(e.keyCode == 13){
			$(this).trigger("enterKey");
		}
	});


	$("#super-submit").click(function(){
        $.post($('#addbookurl').val(),
          {
            title: $("#title").val(),
            author: $("#author").val(),
            press: $("#press").val(),
            title_other: $("#title_other").val(),
            pub_year_origin: $("#pub_year_origin").val(),
            pub_year: $("#pub_year").val(),
            revision: $("#revision").val(),
            revision_origin: $("#revision_origin").val(),
            ISBN: $("#ISBN").val(),
            translator: $("#translator").val(),
            duration: $("#duration").val(),
            
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
          },
        function(res){
        	
        		var obj = $.parseJSON(res);
    			var txt = null;
				if(obj.status == 'Error'){
					txt = '<tr><td><div class="alert alert-danger"><strong>Error!</strong> ' 
							+ 'err: <strong>' + obj.err 
							+ '</strong></div></td></tr>';
				} else if(obj.status == 'OK'){
					txt = '<tr><td><div class="alert alert-success">' 
							+ '<strong> OK！'
							+ '</strong>到 <strong>' + '<a href="'+obj.permalink+'" target="_blank">这里</a> '
							+ '</strong>添加《'+$("#title").val()+'》的拷贝<a name="notice"></a></div></td></tr>';
				}
				$('#super-body').append(txt);
				$('#super-body').focus();

        });
      });

	$('#fixbookinfo-form').submit(function(e){
		console.log('hahha');
		e.preventDefault();
		$('#super-submit').click();
	});
	

}); // end of window