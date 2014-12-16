$(document).ready(
	function(){
		csrftoken = getCookie('csrftoken');

		$('.choose-user-item').click(function(){
			var passurl = $(this).attr('passurl');
			csrftoken = getCookie('csrftoken');

			var that = this;
			$.post(
				passurl,
				{
					'csrfmiddlewaretoken':csrftoken
				},
				function(data){
					var obj = $.parseJSON(data);
					if(obj.status == 'Error'){
						alert('噢哟！ ' + 'Error: ' + obj.err + (obj.message?(' Message: ' + obj.message):""));
						$(that).removeClass('btn-default');
						$(that).addClass('btn-danger');
						$(that).text("审批失败");
						$(that).attr("disabled", "disabled");
					} else if(obj.status == 'OK'){
						$(that).removeClass('btn-default');
						$(that).addClass('btn-success');
						$(that).text("审批成功");
						$(that).attr("disabled", "disabled");
					}
				}
			);
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

		$('#magic2').click(function(){
	    	csrftoken = getCookie('csrftoken');

	    	var curl = $('#find-user-url2').val();
	    	var search = $('#find-user-input2').val();

	    	$('#find-user-tbody2').load(
	    		curl+search, 
	    		function(){
	    			$('.choose-user-down').click(function(){
	    				var downurl = $(this).attr('downurl');
						csrftoken = getCookie('csrftoken');

						var that = this;
						$.post(
							downurl,
							{
								'csrfmiddlewaretoken':csrftoken
							},
							function(data){
								var obj = $.parseJSON(data);
								if(obj.status == 'Error'){
									alert('噢哟！ ' + 'Error: ' + obj.err + (obj.message?(' Message: ' + obj.message):""));
									$(that).removeClass('btn-default');
									$(that).addClass('btn-danger');
									$(that).text("审批失败");
									$(that).attr("disabled", "disabled");
								} else if(obj.status == 'OK'){
									$(that).removeClass('btn-default');
									$(that).addClass('btn-success');
									$(that).text("审批成功");
									$(that).attr("disabled", "disabled");
								}
							}
						);							
					});
	    		}
	    	);
	    	return false;
	    });


		// the form used for fixing book info
		$('#makemypost-form').submit(function(e){
			e.preventDefault();
			$('#makemypost-submit').click();
		});
		$('#makemypost-submit').click(function(){
			var herr = false;
			$('#makemypost-warning').addClass('hidden');
			$('#makemypost-form > .form-group').each(function(){
				var txt = $(this).find('input, textarea').val();
				console.log($.trim($(this).find('.control-label').text()) + ':' + txt);
				if(!txt || !txt.length){
					// empty
					$(this).addClass('has-error');
					$('#makemypost-warning > div').html('噢哟！[ <strong>' + $.trim($(this).text()) + '</strong> ]您还没有填写哟！');
					$('#makemypost-warning').removeClass('hidden');
					herr = true;
					return false;
				} else {
					$('#makemypost-warning').addClass('hidden');
					$(this).removeClass('has-error');
				}
			});

			if(herr)
				return false;

			// check all radio
			var rate = $("input[name='optionsRadios']:checked").val();
			console.log('rate:' + rate);
			if(rate && (rate == "news" || rate == "guide")){
				$('#makemypost-warning').addClass('hidden');
				$(this).removeClass('has-error');
				console.log('meow');
			} else {
				// didn't rate
				$(this).addClass('has-error');
				$('#makemypost-warning > div').html('噢哟！[ <strong>' + $.trim($("label[for='inputRate']").text()) + '</strong> ]您还没有填写哟！');
				$('#makemypost-warning').removeClass('hidden');
				return false;
			}

			var title = $('#input-post-title').val();
			var content = $('#input-post').val();
			var curl = $('#input-post-url').val();

			csrftoken = getCookie('csrftoken');
			$.post(
				curl,
				{
					'csrfmiddlewaretoken' : csrftoken,
					'title' : title,
					'content' : content,
					'species' : rate,
				},
				function(data){
					console.log('get data: ' + data);
					var obj = $.parseJSON(data);
					if(obj.status == 'Error'){
						$('#makemypost-warning > div').html('噢哟！ ' + obj.err);
						$('#makemypost-warning').removeClass('hidden');
					} else if(obj.status == 'OK'){
						$('#makemypost-success').removeClass('hidden');
						setTimeout(
							function(){
								location.reload();
							},
							1000
						);
					}
				}
			);
		});
	}
);