<%include file="/header.mako" />

<div class="col-md mt-4">
	<h1 class="mt-3">Dataset information</h1>
	<p>Specify the dataset information.</p>

	<form action="/submit" method="post">
		<div class="form-group">
			<label for="name">What is the name of this dataset?</label>
			<input type="text" class="form-control" name="displayname" id="name" required placeholder="Dataset name">
		</div>

		<p class="mt-4">Are the column names correctly linked?</p>

		<table class="table table-bordered table-hover">
			<thead>
				<tr>
					<th scope="col">Original column name</th>
					<th scope="col">Standardized column name</th>
				</tr>
			</thead>
			<tbody>
				% for i, column in enumerate(columns):
				<tr>
					<td>${column}</td>
					<td>
						<select class="form-control" name="column">
							<optgroup label="General">
							% for standardColumn in standardColumns:
								%if standardColumn['isCategory'] == '1':
								</optgroup>
								<optgroup label="${standardColumn['description']}">
								% elif standardColumn['id'] == sugestedColumns[i]:
								<option value="${standardColumn['id']}" selected>${standardColumn['description']}</option>
								% else:
								<option value="${standardColumn['id']}">${standardColumn['description']}</option>
								% endif
							% endfor
							</optgroup>
						</select>
					</td>
				</tr>
				% endfor
			</tbody>
		</table>

		<input type="hidden" name="filename" value="${filename}">

		<button type="submit" class="btn btn-primary mt-4">Save dataset</button>
	</form>
</div>

<%include file="/footer.mako" />