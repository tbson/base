# BASE PROJECT

## Minimum dependencies
Only use really needed one

*Dependencies*

- `antd`: All in one enterprise UI kit
- `axios`: For HTTP request. We can use `fetch` but most of us familiar with axios
- `date-fns`: For Ant Design date picker and date/time utilities
- `ramda`: general-purpose tookit, currently use for cloning objects only
- `react`: No comment,
- `react-dom`: No comment,
- `react-router-dom`: For routing on client tei,
- `recoil`: Store global state the React way,
- `ttag`: For multiple language

*Dev Dependencies*
- `@vitejs/plugin-react`: Vite plugin for react development,
- `jest`: For unit testing,
- `ttag-cli`: CLI for ttag use for generating, updating, exporting gettext files
- `vite`: Frontend tooling, fast build and hot reloading

## Features

- JSDoc support
- Build in dashboard
- Use React hooks for most of taks
- Recoil help to dealth with global state if needed.
- Multiple language support. `PoEdit` and `makemessages`/`dumpmessages` do all managing tasks.
- Unit test support
- Abstract away HTTP request operations
