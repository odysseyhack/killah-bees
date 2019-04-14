<%include file="/header.mako" />

<div class="col-md-6 mt-4">
	<h1 class="mt-3">Add a dataset</h1>
	<p>Add a new dataset to the platform.</p>

	<form action="/upload" method="post" enctype="multipart/form-data">
		<div clas="form-group">
			<div class="custom-file">
				<input type="file" class="custom-file-input" id="file-input" name="file" required>
				<label class="custom-file-label" for="file-input">Choose file</label>
			</div>
		</div>

		<button type="submit" class="btn btn-primary mt-4">Add dataset</button>
	</form>
</div>

<%include file="/footer.mako" />