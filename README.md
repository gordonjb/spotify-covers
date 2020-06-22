# spotify-covers
Generates Spotify style playlist covers by overlaying images with text, gradients and logos.

## Requirements
* Install Python
* Install Poetry
* Install the font file [`CircularStd-Bold.otf`](CircularStd-Bold.otf) from the repo.
* If you want to generate your own, clear out the cover images from [`images`](images/), and my generated covers from [`images/covers`](images/covers), and replace the contents of [`config/covers.toml`](config/covers.toml).

## Usage
`poetry run covers` - generate the files described by `covers.toml` and save them to `images/covers`

`poetry run show` - generate the files described by `covers.toml` as temporary files and display them

`poetry run test1`/`test1-s`/`test2`/`test3` - generate the files described by `covers.toml` as temporary files and display them, and display overlaid with the specified test image from [`images/test`](images/test)

## Config items
The project uses [TOML](https://github.com/toml-lang/toml) for config, a full reference is at their repo.

### General config
General config items go under the `[config]` heading

| Item          | Description                                                                             |
|---------------|-----------------------------------------------------------------------------------------|
| `output-size` | Specify the dimensions of created images. Takes a single integer, as covers are square. |

### Cover config
Each cover to be generated is an item in the `[[cover]]` array

| Item               | Description                                                                                                                                                                                                                                                                                  |
|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `main-text`        | The main text of the cover. Supports newlines using '\n'. Can be omitted to have no text.                                                                                                                                                                                                    |
| `font-colour`      | A string colour name or # to be used for the text printed from `main-text`. If not provided, text is white by default.                                                                                                                                                                       |
| `sub-text`         | A smaller text line placed above or below the `main-text` on the cover. Unless `sub-text-above` is set to true, text is drawn a short distance below the main text. Supports newlines using '\n'. Can be omitted to have no text.                                                            |
| `sub-font-colour`  | A string colour name or # to be used for the text printed from `sub-text`. If not provided, text is white by default.                                                                                                                                                                        |
| `sub-text-above`   | If set to true, `sub-text` will be drawn a short distance above the `main-text` on the cover.                                                                                                                                                                                                |
| `bg-image`         | The main background image of the cover, as a string of a filename in `images`. Will be resized to fit the dimensions, with excess cut.                                                                                                                                                       |
| `bg-colour`        | A string colour name or # that will be placed behind the `bg-image` (if present). Transparency in the `bg-image` will be preserved.                                                                                                                                                          |
| `scale`            | If specified, instead of the `bg-image` being filled to the cover dimensions, it will instead be scaled to that percentage of the cover dimensions, preserving the aspect ratio.                                                                                                             |
| `position`         | If defined along with `scale`, defines where the scaled image will be aligned. If not defined, the image will be centred. Only current option is "bottom", which aligns the image somewhere around 7/8 of the way down the cover.                                                            |
| `colour-gradient`  | A colour gradient image, as a string of a filename in `images/gradient` minus the extension. Will be resized to fit the dimensions, with excess cut, and blended over a greyscaled copy of the cover with a default opacity of 70%. This can be changed by specifying a `gradient-opacity`.  |
| `gradient-opacity` | If specified, `colour-gradient`images will be blended at that percentage opacity.                                                                                                                                                                                                            |
| `do-not-greyscale` | If set to true, the cover will not be converted to greyscale before a `colour-gradient` is applied.                                                                                                                                                                                          |
| `use-white-logo`   | If set to true, a white version of the Spotify logo will be overlaid instead of the default black logo.                                                                                                                                                                                      |
| `logo-opacity`     | If specified, the Spotify logo will be overlaid at that percentage opacity.  

## Image credits
Gradients have been generated from https://uigradients.com/. To add more gradients, use their download button and save the images to [`images/gradient`](images/gradient).

The gig images are my own photos, minus the front row shot from Creeper, which is from [Rocksound's gallery](https://www.rocksound.tv/photos/view/this-is-what-creepers-final-show-looked-like).

The BBQ shot is from [Matthieu Joannon](https://unsplash.com/@matt_j?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText) on [Unsplash](https://unsplash.com): https://unsplash.com/photos/M9v68_7hEls

Everything else is Google images

## Examples
![BBQ](/images/covers/BBQ.jpg?raw=true "BBQ")![Triage](/images/covers/Triage.jpg?raw=true "Triage")![Thumbs Up](/images/covers/Thumbs%20Up.jpg?raw=true "Thumbs Up")![Screaming Females](/images/covers/Screaming%20Females.jpg?raw=true "Screaming Females")
