<%include file="/header.mako" />

<div class="col-md mt-4">
	<h1 class="mt-3">${fields['name']} - Privacy breach detector</h1>

	<form method="post">
		<div class="form-group">
			<label>Which fields in the dataset ${fields['name']} do you want to check for data breaches?</label>
			% for id, name in fields['columns'].items():
			<div class="form-check">
				<input class="form-check-input" type="checkbox" name="columns" value="${id}" id="column-${id}">
				<label class="form-check-label" for="column-${id}">${name}</label>
			</div>
			% endfor
		</div>

		<button type="submit" class="btn btn-primary mt-4">Detect breaches</button>
	</form>
</div>

<%include file="/footer.mako" />