import React from 'react';
import ReactDOM from 'react-dom';
import PropTypes from 'prop-types';
import './index.css';

class PhotoCard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div className="photo_card">
        <div>{ this.props.name }</div>
        <img className="thumbnail" src={ this.props.src } alt={ this.props.name }/>
        <div className='author'>By: { this.props.author }</div>
      </div>
    );
  }
}
PhotoCard.propTypes = {
  name: PropTypes.string,
  src: PropTypes.string,
  author: PropTypes.string
};

class Pager extends React.Component {
    render () {
        let prevButton;
        let nextButton;

        if ((this.props.page - 1) > 0) {
          prevButton = (
            <button className='pager-prev' onClick={this.props.prevPage}>
              &lt;-
            </button>
          );
        } else {
          prevButton = (
            <button className='pager-prev disabled' disabled='true'>
              &lt;-
            </button>
          );
        }

        if ((this.props.page) < this.props.pages) {
          nextButton = (
            <button className='pager-next' onClick={this.props.nextPage}>
              -&gt;
            </button>
          );
        } else {
          nextButton = (
            <button className='pager-next disabled' disabled='true'>
              -&gt;
            </button>
          );
        }

        return (
            <div className="pager">
                {prevButton}
                <span className='page_number'>
                  {this.props.page} / {this.props.pages}
                </span>
                {nextButton}
            </div>
        );
    }
}
Pager.propTypes = {
  page: PropTypes.number,
  pages: PropTypes.number,
  nextPage: PropTypes.func,
  prevPage: PropTypes.func
};

class PhotoPage extends React.Component {
    createCard(photo) {
        return (
            <PhotoCard
                id={photo.id}
                name={photo.name}
                src={photo.images[0].https_url}
                author={photo.user.username}
            />
        );
    }

    createCards() {
        let cards = [];
        for (let i=0; i < this.props.photos.length; i +=1) {
            cards.push(this.createCard(this.props.photos[i]));
        }

        return cards;
    }

    render() {
        return (
            <div className="photo_page">
              <h3>
                The current most popular {this.props.photos.length} photos on 500px
              </h3>
              {this.createCards()}
            </div>
        );
    }
}
PhotoPage.propTypes = {
  photos: PropTypes.array
};

class Showcase extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            photos: null,
            rpp: 8,
            page: 1,
            pages: 1,
        };
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

        this.getPhotos(target);
    }

    prevPage() {
        let target = this.state.page - 1;
        if (target < 1) {
            return;
        }

        this.getPhotos(target);
    }

    render() {
        if (this.state.photos === null) {
            this.getPhotos(1);
            return 'loading...';
        } else {
            return (
                <div className='showcase'>
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
            );
        }
    }
}
ReactDOM.render(
    <Showcase />,
    document.getElementById('root')
);
