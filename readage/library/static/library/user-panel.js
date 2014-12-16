var cq;

/* 
 * remember to write load code here
 */

$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
	console.log(e.target);
	cq = e.target;
	console.log(e.relatedTarget);
})



$(document).ready(
	function(){

		$('.reborrow-button').click(function(){
			var uid = $(this).attr('uid');
			var bid = $(this).attr('bid');
			var curl = $(this).attr('curl');

			var that = this;

			csrftoken = getCookie('csrftoken');
			$.post(
				curl,
				{
					'csrfmiddlewaretoken' : csrftoken,
				},
				function(data){
					console.log('get reborrow data: ' + data);
					var obj = $.parseJSON(data);
					if(obj.status == 'Error'){
						alert('噢哟！ ' + 'Error: ' + obj.err + (obj.message?(' Message: ' + obj.message):""));
						$(that).removeClass('btn-default');
						$(that).addClass('btn-danger');
						$(that).text("续借失败");
						$(that).attr("disabled", "disabled");
					} else if(obj.status == 'OK'){
						$(that).removeClass('btn-default');
						$(that).addClass('btn-success');
						$(that).text("续借成功");
						$(that).attr("disabled", "disabled");
					}
				}
			);
		});

		$('#addmylevel-submit').click(function(){
			var addurl = $(this).attr('addurl');

			var that = $('[data-target="#addmylevel"]');
			csrftoken = getCookie('csrftoken');
			$.post(
				addurl,
				{
					'csrfmiddlewaretoken' : csrftoken,
				},
				function(data){
					console.log('get addurl data: ' + data);
					var obj = $.parseJSON(data);
					if(obj.status == 'Error'){
						alert('噢哟！ ' + 'Error: ' + obj.err + (obj.message?(' Message: ' + obj.message):""));
						$(that).removeClass('btn-primary');
						$(that).addClass('btn-danger');
						$(that).text("申请提权失败");
						$(that).attr("disabled", "disabled");
						$('#addmylevel').modal('hide');
					} else if(obj.status == 'OK'){
						$(that).removeClass('btn-primary');
						$(that).addClass('btn-success');
						$(that).text("申请提权成功");
						$(that).attr("disabled", "disabled");
						$('#addmylevel').modal('hide');
					}
				}
			);
		});


		$('#changemypass').submit(function(e){
			e.preventDefault();
			$('#changemypass-submit').click();
		});
		$('#changemypass-submit').click(function(){
			var editurl = $(this).attr('editurl');
			var email = $('#changeemail').val();
			var pass0 = $('#changepassword1').val();
			var pass1 = $('#changepassword2').val();
			var pass2 = $('#changepassword3').val();

			csrftoken = getCookie('csrftoken');
			$.post(
				editurl,
				{
					'csrfmiddlewaretoken' : csrftoken,
					'email' : email,
					'pass0' : pass0,
					'pass1' : pass1,
					'pass2' : pass2,
				},
				function(data){
					console.log('get changemypass data: ' + data);
					var obj = $.parseJSON(data);
					if(obj.status == 'Error'){
						alert('噢哟！ 修改信息失败！' + 'Error: ' + obj.err + (obj.message?(' Message: ' + obj.message):""));
					} else if(obj.status == 'OK'){
						alert('修改信息成功！');
						location.reload();
					}
				}
			);

		});// end of 

		csrftoken = getCookie('csrftoken');
		$('.discard-order-btn').click(function(){
			var disurl = $(this).attr('disurl');
			csrftoken = getCookie('csrftoken');

			var that = this;
			$.post(
				disurl,
				{
					'csrfmiddlewaretoken':csrftoken
				},
				function(data){
					var obj = $.parseJSON(data);
					if(obj.status == 'Error'){
						alert('噢哟！ ' + 'Error: ' + obj.err + (obj.message?(' Message: ' + obj.message):""));
						$(that).removeClass('btn-default');
						$(that).addClass('btn-danger');
						$(that).text("取消预约失败");
						$(that).attr("disabled", "disabled");
					} else if(obj.status == 'OK'){
						$(that).removeClass('btn-default');
						$(that).addClass('btn-success');
						$(that).text("取消预约成功");
						$(that).attr("disabled", "disabled");
					}
				}
			);
		});

	}// end of ready function
);