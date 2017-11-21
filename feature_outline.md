## Feature Outline
- [ ] basic flow
- [ ] async
- [ ] parse HTML by beautiful soup 
- [ ] customize middleware
- [ ] pipeline
- [ ] distribution
- [ ] command line tool
- [ ] documentation

## Detail
**basic flow**

Implement a basic flow of web spider. Low coupling and extensible. 
Three main components

* fetcher
* parser
* saver

**async support**

Support async by aiohttp module.
	
**parse HTML**

parse HTML by beautiful soup module

**customize middleware**

customize spider middleware and download middleware, configurable in Config file

**pipeline**

support persistance to file, mysql and mongodb

**distribution support**

distribution, use Redis as a task queue

**command line tool**

provide a command line tool to initialize the project, run the project

**documentation**

add documentation for Crawl_it 