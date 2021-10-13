# **Participons - frontend**

The frontend is using Nuxt.js, a Vue.js based framework. It communicates with the backend API ([branch heroku-backend](https://github.com/vicsim181/P13/tree/heroku-backend)).

## Build Setup

```bash
# install dependencies
$ npm install

# serve with hot reload at localhost:3000
$ npm run dev

# build for production and launch server
$ npm run build
$ npm run start

# generate static project
$ npm run generate
```

For detailed explanation on how things work, check out the [documentation](https://nuxtjs.org).

## Organization of the project

Various folders are used here, the main ones are the `components`, `layouts` and `pages`.

The Components are elements that can be used in different pages, for example the navbar or the footer. In order to avoid repetition of the code used to build them in each pages of the website, we create them as Components and add them to the pages.

The Layouts are general templates which can be applied to all the pages, once again with the objective to avoid repetition of the same code in different files. The `default.vue` file gives the default presentation of all the pages of the website, including the navbar and the footer.

The Pages will be called inside the `default.vue` in `<Nuxt></Nuxt>`. Therefore you can custom what is going to be placed in addition of the default layout. Pages can include components and proper html/css or Javascript elements.

To know more in details how to order and use the different folders, check the [documentation](https://nuxtjs.org/docs/directory-structure/nuxt).
