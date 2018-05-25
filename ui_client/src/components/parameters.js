import React, { Component } from 'react';
import { connect } from 'react-redux';
import { reduxForm, Field } from 'redux-form';
import { toStatusCodeOne, updateParameters, runExperiment } from '../actions/index';

class Parameters extends Component {

  handleFormSubmit(experimentalParameters) {
    // console.log(experimentalParameters);
    this.props.toStatusCodeOne();
    this.props.updateParameters(experimentalParameters);
    this.props.runExperiment(experimentalParameters);
  }

  renderForm(disabled) {

    // these properties comes from ReduxForm
    const { handleSubmit } = this.props;

    return (
      <form onSubmit={handleSubmit(this.handleFormSubmit.bind(this))} className="border p-3 mb-5">

        <div>
          <label><b>1. Algorithm:</b></label>
          <div className="row no-gutter">
            <label className="col-md-2">
              <Field name="algorithm" component="input" type="radio" value="regular_hits" required="required" disabled={disabled} />
              {' '}Regular HITS
            </label>
            <label className="col-md-2">
              <Field name="algorithm" component="input" type="radio" value="multilayered_hits" required="required" disabled={disabled} />
              {' '}Multi-layered HITS
            </label>
          </div>
        </div>

        <div>
          <Field name="query_node_index" component={this.renderInput} type="number" label="2. Query Node Index (-1 represents no query node is specified):" required={true} disabled={disabled} />
        </div>

        <div>
          <label><b>3. Selected Layers:</b></label>
          <div className="row no-gutter">
            <label className="col-md-1">
              <Field name="is_book_selected" component="input" type="checkbox" value="book" disabled={disabled} />
              {' '}Book
            </label>
            <label className="col-md-1">
              <Field name="is_dvd_selected" component="input" type="checkbox" value="dvd" disabled={disabled} />
              {' '}DVD
            </label>
            <label className="col-md-1">
              <Field name="is_music_selected" component="input" type="checkbox" value="music" disabled={disabled} />
              {' '}Music
            </label>
            <label className="col-md-1">
              <Field name="is_video_selected" component="input" type="checkbox" value="video" disabled={disabled} />
              {' '}Video
            </label>
            <label className="col-md-3">
              <Field name="is_customer_selected" component="input" type="checkbox" value="customer" disabled={disabled} />
              {' '}Customer (Knowledge Layer)
            </label>
          </div>
        </div>

        <button action="submit" className="btn btn-primary col-md-1 mt-4" disabled={disabled}>Run</button>
      </form>
    );
  }

  renderInput = (field) => (
    <fieldset className="form-group">
      <label><b>{field.label}</b></label>
      <input
        className="form-control"
        {...field.input}
        type={field.type}
        required={field.required? 'required' : ''}
        disabled={field.disabled? 'disabled' : ''}
      />
    </fieldset>
  );

  render() {

    let disabled = false;
    if (this.props.status_code === 1) {
      disabled = true;
    }

    return (
      <div>
        <h1>Experimental Parameters</h1>
        {this.renderForm(disabled)}
      </div>
    );
  }
}

Parameters = reduxForm({
  form: 'parameters',
})(Parameters);

// Initialization
function mapStateToProps({ status }) {
  return {
    'status_code': status.code,
    initialValues: {
      'is_book_selected': false,
      'is_dvd_selected': false,
      'is_music_selected': false,
      'is_video_selected': false,
      'is_customer_selected': false,
    }
  };
}

export default connect(mapStateToProps, { toStatusCodeOne, updateParameters, runExperiment })(Parameters);