import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

class PhotoCard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    return (
      <div class="photo_card">
        <div>{ this.props.name }</div>
          <img class="thumbnail" src={ this.props.src }/>
        <div class='author'>By: { this.props.author }</div>
      </div>
    )
  }
}

class Pager extends React.Component {
  constructor(props) {
    super(props);
  }

  render () {
    let prevButton;
    let nextButton;

    if ((this.props.page - 1) > 0) {
      prevButton = (
        <button class='pager-prev' onClick={this.props.prevPage}>&lt;-</button>
      )
    } else {
      prevButton = (
        <button class='pager-prev disabled' disabled='true'>&lt;-</button>
      )
    }

    if ((this.props.page) < this.props.pages) {
      nextButton = (
        <button class='pager-next' onClick={this.props.nextPage}>-&gt;</button>
      )
    } else {
      nextButton = (
        <button class='pager-next disabled' disabled='true'>-&gt;</button>
      )
    }

    return (
      <div class="pager">
      {prevButton}
      <span class='page_number'>{this.props.page} / {this.props.pages}</span>
      {nextButton}
      </div>
    )
  }
}

class PhotoPage extends React.Component {
  createCard(photo) {
    return (
      <PhotoCard
        id={photo.id}
        name={photo.name}
        src={photo.images[0].https_url}
        author={photo.user.username}
      />
    )
  }

  createCards() {
    let cards = []
    for (let i=0; i < this.props.photos.length; i +=1) {
      cards.push(this.createCard(this.props.photos[i]));
    }

    return cards;
  };

  render() {
    return (
      <div class="photo_page">
        <h3>The current most popular {this.props.photos.length} photos on 500px</h3>

        {this.createCards()}

      </div>
    )
  }
}

class Showcase extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      photos: null,
      rpp: 8,
      page: 1,
      pages: 1,
    }

  }

  getPhotos(page) {
    let url = '/bff/?rpp=' + this.state.rpp + '&page=' + page;

    window.fetch(url).then((response) => {
      return response.json();
    }).then((blob) => {
      this.setState({
        photos: blob.photos,
        page: blob.current_page,
        pages: blob.total_pages
      });
    });
  }

  nextPage() {
    let target = this.state.page + 1;
    if (target > this.state.pages) {
      return;
    }

    this.setState({
      page: target,
    })
    this.getPhotos(target)
  }

  prevPage() {
    let target = this.state.page - 1;
    if (target < 1) {
      return;
    }

    this.getPhotos(target)
  }

  render() {
    if (this.state.photos === null) {
      this.getPhotos(1);
      return 'loading...';
    } else {
      return (
        <div class='showcase'>
          <PhotoPage
            photos={this.state.photos}
            page={this.state.page}
            rpp={this.state.rpp}
          />
          <Pager
            page={this.state.page}
            pages={this.state.pages}
            nextPage={() => this.nextPage()}
            prevPage={() => this.prevPage()}
          />
        </div>
      )
    }
  }
}
ReactDOM.render(
  <Showcase />,
  document.getElementById('root')
);
