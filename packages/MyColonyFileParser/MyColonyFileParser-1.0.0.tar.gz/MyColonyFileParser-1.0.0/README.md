# mcfp - My Colony File Parser

  [![DeepSource](https://deepsource.io/gh/MCW-My-Colony-Wiki/MyColonyFileParser.svg/?label=active+issues&show_trend=true&token=zjOyAP4RLEuWcm5YOU1NQJW_)](https://deepsource.io/gh/MCW-My-Colony-Wiki/MyColonyFileParser/?ref=repository-badge)
  
  [中文版readme](README_zh.md)
  
  current not suppot My Colony 2

## Index of content

- [Config](#config)
- [Classes](#classes)
  - [Base](#base)
    - [CommonBase](#commonbase)
    - [DictBase](#dictbase)
    - [ListBase](#listbase)
  - [FileBase](#filebase)
    - [Game](#game)
    - [Strings](#strings)
  - [CategoryBase](#categorybase)
    - [DictCategory](#dictcategory)
    - [ListCategory](#listcategory)
  - [UnitBase](#unitbase)
    - [DictUnit](#dictunit)
    - [ListUnit](#listunit)
- [Exceptions](#exceptions)
  - [MCFPError](#mcfperror)
    - [FileError](#fileerror)
      - [InvalidFileChannel](#invalidfilechannel)
      - [InvalidFileVersion](#invalidfileversion)
      - [InvalidFileName](#invalidfilename)
    - [CategoryError](#categoryerror)
      - [InvalidCategoryName](#invalidcategoryname)
    - [UnitError](#uniterror)
      - [InvalidUnitName](#invalidunitname)

## Config

- Description: this module use `configparser` that in stdlib to provide config function
- Path: `mcfp.config.config`
- Sections
  - `network`
    - Options
      - `timeout`(int, default=3): timeout of all the network related function

## Classes

### Base

#### CommonBase

- Description: provide generic method
- Path: `mcfp.base.CommonBase`
- Method
  - `__delattr__`: disable `del object.attr`
  - `__str__`: return `self.name`

#### DictBase

- Description: provide method of `dict` object
- Path: `mcfp.base.DictBase`
- Inherit: [CommonBase](#commonbase)

#### ListBase

- Description: provide method of `list` object
- Path: `mcfp.base.ListBase`
- Inherit: [CommonBase](#commonbase)

### FileBase

- Description: basically same as `dict` object
- Path: `mcfp.filebase.FileBase`
- Inherit: [DictBase](#dictbase)
- Attributes
  - `name`: file name
  - `dict`: file data
- Method
  - `categories`: alias of `file.keys()`

#### Game

- Description: represents files like [game.js](https://www.apewebapps.com/apps/my-colony/1.14.0/game.js)
- Path: `mcfp.file.Game`
- Inherit: [FileBase](#filebase)

#### Strings

- Description: represents files like [strings.js](https://www.apewebapps.com/apps/my-colony/1.14.0/strings.js)
- Path: `mcfp.file.Strings`
- Inherit: [FileBase](#filebase)

### CategoryBase

- Path: `mcfp.categorybase.CategoryBase`
- Common attributes
  - `file`: instance of subclass of FileBase which this category belong
  - `name`: category name
  - `data`: category data
- Common method
  - `units`: Implemented by subclass

#### DictCategory

- Description: basically same as `dict` object
- Path: `mcfp.category.DictCategory`
- Inherit: [DictBase](#dictbase), [CategoryBase](#categorybase)
- Attributes
  - `dict`: alias of `self.data`
- Method
  - `units`: alias of `self.keys`

#### ListCategory

- Description: basically same as `list` object
- Path: `mcfp.category.ListCategory`
- Inherit: [ListBase](#listbase), [CategoryBase](#categorybase)
- Attributes
  - `list`: alias of `self.data`
- Method
  - `units`: similar with `self.__iter__` but return str object

### UnitBase

- Path: `mcfp.unitbase.UnitBase`
- Common attributes
  - `file`: instance of subclass of FileBase which this unit belong, same as `category.file`
  - `category`: instance of subclass of CategoryBase which this unit belong
  - `data`: unit data

#### DictUnit

- Description: basically same as `dict` object
- Path: `mcfp.unit.DictUnit`
- Inherit: [DictBase](#dictbase), [UnitBase](#unitbase)

#### ListUnit

- Description: basically same as `list` object
- Path: `mcfp.unit.ListUnit`
- Inherit: [ListBase](#listbase), [UnitBase](#unitbase)

## Excpetions

### MCFPError

Base exception of MCFP

- Inherit: [Exception](https://docs.python.org/3/library/exceptions.html#Exception)

### FileError

File related error

- Inherit: [MCFPerror](#mcfperror)

### InvalidFileChannel

Invalid file channel

- Inherit: [FileError](#fileerror)

### InvalidFileVersion

Invalid file version

- Inherit: [FileError](#fileerror)

### InvalidFileName

Invalid file name

- Inherit: [FileError](#fileerror)

### CategoryError

Category related error

- Inherit: [MCFPError](#mcfperror)

### InvalidCategoryName

Invalid category name

- Inherit: [CategoryError](#categoryerror)

### UnitError

Unit related error

- Inherit: [MCFPError](#mcfperror)

### InvalidUnitName

Invalid unit name

- Inherit: [UnitError](#uniterror)
