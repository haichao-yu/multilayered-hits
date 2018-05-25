import React, { Component } from 'react';
import { connect } from 'react-redux';
import { reduxForm, Field } from 'redux-form';
import { submitRatings } from '../actions/index';

class Results extends Component {

  handleFormSubmit(ratings) {
    this.props.submitRatings(this.props.parameters, ratings);
  }

  renderResults() {

    // let { top_K_products } = this.props.results;
    let { status_code } = this.props;

    if (status_code === 0) {
      return (
        <div className="alert alert-primary mt-4" role="alert">
          Please run experiment to see results.
        </div>
      );
    }

    if (status_code === 1) {
      return (
        <div className="alert alert-warning mt-4" role="alert">
          The experiment is running. This may take couple of seconds.
        </div>
      );
    }

    if (status_code === 3) {
      return (
        <div className="alert alert-success mt-4" role="alert">
          You have submitted your ratings. Now you can run another experiment.
        </div>
      );
    }

    // status_code === 2
    return (
      <div>
        <h4 className="mb-2">Query Product</h4>
        {this.renderQueryProduct()}
        <h4 className="mb-4">Top K Ranked Products</h4>
        {this.renderTopKProducts()}
      </div>
    );
  }

  renderQueryProduct() {
    let query_product = this.props.results.query_product;
    if (!query_product) {
      return <p>None</p>;
    }
    return <p>{query_product.group}: <a href={query_product.link} target="_blank">{query_product.title}</a></p>;
  }

  renderTopKProducts() {

    // these properties comes from ReduxForm
    const { handleSubmit } = this.props;

    let top_K_products = this.props.results.top_K_products;
    return (
      <form onSubmit={handleSubmit(this.handleFormSubmit.bind(this))}>
        {top_K_products.map((data) => {
          return (
            <div key={data.group} className="mb-4">
              {this.renderTable(data)}
              <div>
                {this.renderText(data.group, 'authority')}
                {this.renderRadio(data.group, 'authority')}
              </div>
              <div>
                {this.renderText(data.group, 'hub')}
                {this.renderRadio(data.group, 'hub')}
              </div>
            </div>
          );
        })}
        <button action="submit" className="btn btn-primary mb-5">Submit Your Ratings</button>
      </form>
    );
  }

  renderTable(data) {
    return (
      <div>
        <h6>{data.group.toUpperCase()}:</h6>
        <table className="table table-striped">
          <thead className="thead-dark">
            <tr>
              <th className="d-inline-block col-2">Rank</th>
              <th className="d-inline-block col-5">Authority</th>
              <th className="d-inline-block col-5">Hub</th>
            </tr>
          </thead>
          <tbody>
            {data.products.map((product) => {
              return this.renderRow(product);
            })}
          </tbody>
        </table>
      </div>
    );
  }

  renderRow(product) {
    return (
      <tr key={product.rank}>
        <th className="d-inline-block col-2">{product.rank}</th>
        <th className="d-inline-block col-5"><a href={product.authority.link} target='_blank'>{product.authority.title}</a></th>
        <th className="d-inline-block col-5"><a href={product.hub.link} target='_blank'>{product.hub.title}</a></th>
      </tr>
    )
  }

  renderText(group, ranking_metric) {
    if (group === 'book') {
      return <div>Relevance of top-K ({ranking_metric}) ranked {group.toUpperCase()}s (1 is least relevant, 5 is most relevant):</div>
    }
    else {
      return <div>Helpfulness of top-K ({ranking_metric}) ranked {group.toUpperCase()}s in terms of interpreting top-K ({ranking_metric}) ranked BOOKs (1 is least helpful, 5 is most helpful):</div>
    }
  }

  renderRadio(group, ranking_metric) {
    let ratings = [1, 2, 3, 4, 5];
    return ratings.map((rating) => {
      return (
        <label key={rating} className="col-md-1">
          <Field name={'rating_'.concat(group, '_', ranking_metric)} component="input" type="radio" value={String(rating)} required="required" /> {rating}
        </label>
      )
    })
  }

  render() {
    return (
      <div>
        <h1>Experimental Results</h1>
        {this.renderResults()}
      </div>
    );
  }
}

Results = reduxForm({
  form: 'ratings',
})(Results);

function mapStateToProps({ status, parameters, results }) {
  return {
    'status_code': status.code,
    'parameters': parameters,
    'results': results,
  };
}

export default connect(mapStateToProps, { submitRatings })(Results);