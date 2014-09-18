(function($){

	$('select[name="fld_pid"]').change(function(){
		if($(this).val()!=""){
				$.getJSON( './json/article_class.json.php', {pid:$(this).val()}, function(data){
					if(data.stat){
						$('select[name="fld_cid"]').html('');
						$('select[name="fld_cid"]').append('<option value="">--Select--</option>');
						for(i=0; i<data.list.length; i++){
							$('select[name="fld_cid"]').append('<option value="'+data.list[i].id+'">'+data.list[i].name+'('+data.list[i].name2+')'+'</option>');
						}
					}
				});
		}
	});

	if ($('#img_upload').length>0){
		new AjaxUpload( '#img_upload', {
			action:'/upload/image',
			name:'file_upload',
			responseType:'json',
			onSubmit:function(file, ext){
				if( ext && !(/^(jpg|png|jpeg|gif|bmp)$/.test(ext)) ){
					alert("上传文件类弄型不正确");
					return false;
				}
				return true;
			},
			onComplete:function(file, data){
				if(data.stat){
					$("input[name='picture']").val(data.url);
				}
				else{
					alert(data.msg);
				}
			}
		});
	}

	if ($('textarea[name="content"]').length>0){
		var editor = KindEditor.create('textarea[name="content"]', {
			themeType:'simple',
			allowFileManager:true,
			cssPath:'/static/js/kindeditor/plugins/code/prettify.css',
			uploadJson:'/kindeditor/upload',
			fileManagerJson:'/kindeditor/filemanager',
			//items:['source', '|', 'cut', 'copy', 'paste', 'plainpaste', 'wordpaste', '|', 'image', 'multiimage', 'flash', 'media', 'insertfile', 'table', 'link', 'unlink', '|', 'clearhtml', 'fullscreen', '/', 'formatblock', 'fontname', 'fontsize', '|', 'font-color', 'hilitecolor', 'blod', 'italic', 'underline', 'removeformat', 'justifyleft', 'justifycenter', 'justifyright', 'justifyfull', 'insertorderedlist', 'insertunorderedlist', 'indent', 'outdent']
		});
	}
	
	function field_value(table, field, value, id){
		var stat = false;
		if(table!='' && field!='' && value!=''){
			$.ajax({
				url:'/field', 
				data:'table='+table+'&field='+field+'&value='+value+'&id='+id, 
				async:false,
				dataType:'json',
				success:function(data){
					stat = data.has;
				}
			});	
		}
		return stat;
	}



	// form validate
	$('[name="group_add"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		if ($('[name="name"]').val()==''){
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('用户组名称不能为空!');	
			stat=false;
		}
		if (field_value('group', 'name', $('[name="name"]').val(), 0)) {
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('用户组名称已经存在!')	
			stat=false;
		}	
		return stat;
	});
	$('[name="group_edit"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		if ($('[name="name"]').val()==''){
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('用户组名称不能为空!')	
			stat=false;
		}	
		if (field_value('group', 'name', $('[name="name"]').val(), $('[name="id"]').val())) {
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('用户组名称已经存在!')	
			stat=false;
		}	
		return stat;
	});
	$('[name="user_add"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		if ($('[name="username"]').val()==''){
			if ($('[name="username"]').parent().children('span.msg').length==0) {
				$('[name="username"]').parent().append('<span class="msg"></span>');
			}
			$('[name="username"]').parent().children('span.msg').html('用户名不能为空!')	
			stat=false;
		}	
		if ($('[name="email"]').val()==''){
			if ($('[name="email"]').parent().children('span.msg').length==0) {
				$('[name="email"]').parent().append('<span class="msg"></span>');
			}
			$('[name="email"]').parent().children('span.msg').html('邮箱不能为空!')	
			stat=false;
		}	
		if ($('[name="password"]').val()==''){
			if ($('[name="password"]').parent().children('span.msg').length==0) {
				$('[name="password"]').parent().append('<span class="msg"></span>');
			}
			$('[name="password"]').parent().children('span.msg').html('密码不能为空!')	
			stat=false;
		}	
		if ($('[name="password_confirm"]').val()==''){
			if ($('[name="password_confirm"]').parent().children('span.msg').length==0) {
				$('[name="password_confirm"]').parent().append('<span class="msg"></span>');
			}
			$('[name="password_confirm"]').parent().children('span.msg').html('重复密码不能为空!')	
			stat=false;
		}	
		if ($('[name="password_confirm"]').val()!=$('[name="password"]').val()){
			if ($('[name="password"]').parent().children('span.msg').length==0) {
				$('[name="password"]').parent().append('<span class="msg"></span>');
			}
			$('[name="password"]').parent().children('span.msg').html('两次输入的密码不一致!')	
			stat=false;
		}	
		if (field_value('user', 'username', $('[name="username"]').val(), 0)) {
			if ($('[name="username"]').parent().children('span.msg').length==0) {
				$('[name="username"]').parent().append('<span class="msg"></span>');
			}
			$('[name="username"]').parent().children('span.msg').html('用户名已经存在!')	
			stat=false;
		}	
		if (field_value('user', 'email', $('[name="email"]').val(), 0)) {
			if ($('[name="email"]').parent().children('span.msg').length==0) {
				$('[name="email"]').parent().append('<span class="msg"></span>');
			}
			$('[name="email"]').parent().children('span.msg').html('邮箱已经存在!')	
			stat=false;
		}	
		return stat;
	});
	$('[name="user_edit"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		if ($('[name="username"]').val()==''){
			if ($('[name="username"]').parent().children('span.msg').length==0) {
				$('[name="username"]').parent().append('<span class="msg"></span>');
			}
			$('[name="username"]').parent().children('span.msg').html('用户名不能为空!')	
			stat=false;
		}	
		if ($('[name="email"]').val()==''){
			if ($('[name="email"]').parent().children('span.msg').length==0) {
				$('[name="email"]').parent().append('<span class="msg"></span>');
			}
			$('[name="email"]').parent().children('span.msg').html('邮箱不能为空!')	
			stat=false;
		}
		if ($('[name="password_old"]').val()!=''){
			if ($('[name="password"]').val()==''){
				if ($('[name="password"]').parent().children('span.msg').length==0) {
					$('[name="password"]').parent().append('<span class="msg"></span>');
				}
				$('[name="password"]').parent().children('span.msg').html('新密码不能为空!')	
				stat=false;
			}	
			if ($('[name="password_confirm"]').val()==''){
				if ($('[name="password_confirm"]').parent().children('span.msg').length==0) {
					$('[name="password_confirm"]').parent().append('<span class="msg"></span>');
				}
				$('[name="password_confirm"]').parent().children('span.msg').html('重复新密码不能为空!')	
				stat=false;
			}	
			if ($('[name="password_confirm"]').val()!=$('[name="password"]').val()){
				if ($('[name="password"]').parent().children('span.msg').length==0) {
					$('[name="password"]').parent().append('<span class="msg"></span>');
				}
				$('[name="password"]').parent().children('span.msg').html('两次输入的新密码不一致!')	
				stat=false;
			}	
		}
		if (field_value('user', 'username', $('[name="username"]').val(), $('[name="id"]').val())) {
			if ($('[name="username"]').parent().children('span.msg').length==0) {
				$('[name="username"]').parent().append('<span class="msg"></span>');
			}
			$('[name="username"]').parent().children('span.msg').html('用户名已经存在!')	
			stat=false;
		}	
		if (field_value('user', 'email', $('[name="email"]').val(), $('[name="id"]').val())) {
			if ($('[name="email"]').parent().children('span.msg').length==0) {
				$('[name="email"]').parent().append('<span class="msg"></span>');
			}
			$('[name="email"]').parent().children('span.msg').html('邮箱已经存在!')	
			stat=false;
		}
		return stat;
	});

	$('[name="article_class_add"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		if ($('[name="name"]').val()==''){
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('分类名称不能为空!')	
			stat=false;
		}	
		if (field_value('acticle_class', 'name', $('[name="name"]').val(), 0)) {
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('分类名称已经存在!')	
			stat=false;
		}	
		return stat;
	});
	$('[name="article_class_edit"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		if ($('[name="name"]').val()==''){
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('分类名称不能为空!')	
			stat=false;
		}	
		if (field_value('acticle_class', 'name', $('[name="name"]').val(), $('[name="id"]').val())) {
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('分类名称已经存在!')	
			stat=false;
		}	
		return stat;
	});

	$('[name="product_class_add"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		if ($('[name="name"]').val()==''){
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('分类名称不能为空!')	
			stat=false;
		}	
		if (field_value('product_class', 'name', $('[name="name"]').val(), 0)) {
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('分类名称已经存在!')	
			stat=false;
		}	
		return stat;
	});
	$('[name="product_class_edit"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		if ($('[name="name"]').val()==''){
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('分类名称不能为空!')	
			stat=false;
		}	
		if (field_value('product_class', 'name', $('[name="name"]').val(), $('[name="id"]').val())) {
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('分类名称已经存在!')	
			stat=false;
		}	
		return stat;
	});

	$('[name="picture_class_add"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		if ($('[name="name"]').val()==''){
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('分类名称不能为空!')	
			stat=false;
		}	
		if (field_value('picture_class', 'name', $('[name="name"]').val(), 0)) {
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('分类名称已经存在!')	
			stat=false;
		}	
		return stat;
	});
	$('[name="picture_class_edit"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		if ($('[name="name"]').val()==''){
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('分类名称不能为空!')	
			stat=false;
		}	
		if (field_value('picture_class', 'name', $('[name="name"]').val(), $('[name="id"]').val())) {
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('分类名称已经存在!')	
			stat=false;
		}	
		return stat;
	});
	
	$('[name="article_add"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		editor.sync();
		if ($('[name="title"]').val()==''){
			if ($('[name="title"]').parent().children('span.msg').length==0) {
				$('[name="title"]').parent().append('<span class="msg"></span>');
			}
			$('[name="title"]').parent().children('span.msg').html('标题不能为空!')	
			stat=false;
		}	
		if ($('[name="content"]').val()==''){
			if ($('[name="content"]').parent().children('span.msg').length==0) {
				$('[name="content"]').parent().prepend('<span class="msg"></span>');
			}
			$('[name="content"]').parent().children('span.msg').html('内容不能为空!')	
			stat=false;
		}	
		if (field_value('article', 'title', $('[name="title"]').val(), 0)) {
			if ($('[name="title"]').parent().children('span.msg').length==0) {
				$('[name="title"]').parent().append('<span class="msg"></span>');
			}
			$('[name="title"]').parent().children('span.msg').html('标题已经存在!')	
			stat=false;
		}	
		return stat;
	});
	$('[name="article_edit"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		editor.sync();
		if ($('[name="title"]').val()==''){
			if ($('[name="title"]').parent().children('span.msg').length==0) {
				$('[name="title"]').parent().append('<span class="msg"></span>');
			}
			$('[name="title"]').parent().children('span.msg').html('标题不能为空!')	
			stat=false;
		}	
		if ($('[name="content"]').val()==''){
			if ($('[name="content"]').parent().children('span.msg').length==0) {
				$('[name="content"]').parent().prepend('<span class="msg"></span>');
			}
			$('[name="content"]').parent().children('span.msg').html('内容不能为空!')	
			stat=false;
		}	
		if (field_value('article', 'title', $('[name="title"]').val(), $('[name="id"]').val())) {
			if ($('[name="title"]').parent().children('span.msg').length==0) {
				$('[name="title"]').parent().append('<span class="msg"></span>');
			}
			$('[name="title"]').parent().children('span.msg').html('标题已经存在!')	
			stat=false;
		}	
		return stat;
	});

	$('[name="product_add"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		editor.sync();
		if ($('[name="name"]').val()==''){
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('名称不能为空!')	
			stat=false;
		}	
		if ($('[name="content"]').val()==''){
			if ($('[name="content"]').parent().children('span.msg').length==0) {
				$('[name="content"]').parent().prepend('<span class="msg"></span>');
			}
			$('[name="content"]').parent().children('span.msg').html('内容不能为空!')	
			stat=false;
		}	
		if (field_value('product', 'name', $('[name="name"]').val(), 0)) {
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('名称已经存在!')	
			stat=false;
		}	
		return stat;
	});
	$('[name="product_edit"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		editor.sync();
		if ($('[name="name"]').val()==''){
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('名称不能为空!')	
			stat=false;
		}	
		if ($('[name="content"]').val()==''){
			if ($('[name="content"]').parent().children('span.msg').length==0) {
				$('[name="content"]').parent().prepend('<span class="msg"></span>');
			}
			$('[name="content"]').parent().children('span.msg').html('内容不能为空!')	
			stat=false;
		}	
		if (field_value('picture', 'name', $('[name="name"]').val(), $('[name="id"]').val())) {
			if ($('[name="name"]').parent().children('span.msg').length==0) {
				$('[name="name"]').parent().append('<span class="msg"></span>');
			}
			$('[name="name"]').parent().children('span.msg').html('名称已经存在!')	
			stat=false;
		}	
		return stat;
	});

	$('[name="picture_add"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		editor.sync();
		if ($('[name="title"]').val()==''){
			if ($('[name="title"]').parent().children('span.msg').length==0) {
				$('[name="title"]').parent().append('<span class="msg"></span>');
			}
			$('[name="title"]').parent().children('span.msg').html('名称不能为空!')	
			stat=false;
		}	
		if ($('[name="content"]').val()==''){
			if ($('[name="content"]').parent().children('span.msg').length==0) {
				$('[name="content"]').parent().prepend('<span class="msg"></span>');
			}
			$('[name="content"]').parent().children('span.msg').html('内容不能为空!')	
			stat=false;
		}	
		if (field_value('picture', 'title', $('[name="title"]').val(), $('[name="id"]').val())) {
			if ($('[name="title"]').parent().children('span.msg').length==0) {
				$('[name="title"]').parent().append('<span class="msg"></span>');
			}
			$('[name="title"]').parent().children('span.msg').html('标题已经存在!')	
			stat=false;
		}	
		return stat;
	});
	$('[name="picture_edit"]').submit(function(){
		stat = true;
		$("span.msg").html('');
		editor.sync();
		if ($('[name="title"]').val()==''){
			if ($('[name="title"]').parent().children('span.msg').length==0) {
				$('[name="title"]').parent().append('<span class="msg"></span>');
			}
			$('[name="title"]').parent().children('span.msg').html('名称不能为空!')	
			stat=false;
		}	
		if ($('[name="content"]').val()==''){
			if ($('[name="content"]').parent().children('span.msg').length==0) {
				$('[name="content"]').parent().prepend('<span class="msg"></span>');
			}
			$('[name="content"]').parent().children('span.msg').html('内容不能为空!')	
			stat=false;
		}	
		if (field_value('picture', 'title', $('[name="title"]').val(), $('[name="id"]').val())) {
			if ($('[name="title"]').parent().children('span.msg').length==0) {
				$('[name="title"]').parent().append('<span class="msg"></span>');
			}
			$('[name="title"]').parent().children('span.msg').html('名称已经存在!')	
			stat=false;
		}	
		return stat;
	});
	$('[name="form_password"]').submit(function(){
		stat = true;
		if ($('[name="password_old"]').val()==''){
			$('[name="password_old"]').parent().children('span.msg').html('旧密码不能为空!')	
			stat=false;
		}
		if ($('[name="password"]').val()==''){
			if ($('[name="password"]').parent().children('span.msg').length==0) {
				$('[name="password"]').parent().append('<span class="msg"></span>');
			}
			$('[name="password"]').parent().children('span.msg').html('新密码不能为空!')	
			stat=false;
		}	
		if ($('[name="password_confirm"]').val()==''){
			if ($('[name="password_confirm"]').parent().children('span.msg').length==0) {
				$('[name="password_confirm"]').parent().append('<span class="msg"></span>');
			}
			$('[name="password_confirm"]').parent().children('span.msg').html('重复新密码不能为空!')	
			stat=false;
		}	
		if ($('[name="password_confirm"]').val()!=$('[name="password"]').val()){
			if ($('[name="password"]').parent().children('span.msg').length==0) {
				$('[name="password"]').parent().append('<span class="msg"></span>');
			}
			$('[name="password"]').parent().children('span.msg').html('两次输入的新密码不一致!')	
		}	
		return stat;
	});

	$('[name="form_config"]').submit(function(){
		stat = true;
		if ($('[name="sitename"]').val()==''){
			$('[name="sitename"]').parent().children('span.msg').html('站点名称不能为空!')	
			stat=false;
		}
		return stat;
	});
})(jQuery);
