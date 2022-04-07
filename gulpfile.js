// let project_folder = 'dist';
let project_folder = 'staticfiles';
let source_folder = '#assets';
// let images_folder = 'images';
// let media_folder = 'media';

let fs = require('fs');

let path = {
    build: {
        css: `./${project_folder}/css`,
        js:  `./${project_folder}/js`,
        img: `./${project_folder}/img`,
        // images: `${images_folder}/`,
        fonts: `./${project_folder}/fonts`
    },
    src: {
        css: `./${source_folder}/#scss/style.scss`,
        js:  `./${source_folder}/#js/script.js`,
        img: `./${source_folder}/#img/**/*.{jpg,png,svg,gif,ico,webp}`,
        // images: `${media_folder}/**/*.{jpg,png,svg,gif,ico,webp}`,
        fonts: `./${source_folder}/#fonts/*.{ttf,eot,woff,woff2}`
    },
    watch: {
        css: `${source_folder}/**/*.scss`,
        js:  `${source_folder}/**/*.js`,
        img: `${source_folder}/**/*.{jpg,png,svg,gif,ico,webp}`,
        // images: `${media_folder}/**/*.{jpg,png,svg,gif,ico,webp}`
    },
    clean: `./${project_folder}/`
}

const {src, dest} = require('gulp'),
    gulp = require('gulp'),
    // browsersync = require('browser-sync').create(),
    fileinclude = require('gulp-file-include'),
    del = require('del'), // удаление папки
    scss = require('gulp-sass')(require('sass')),
    autoprefixer = require('gulp-autoprefixer'),
    group_media = require('gulp-group-css-media-queries'),
    clean_css = require('gulp-clean-css')
    rename = require('gulp-rename'),
    uglify = require('gulp-uglify-es').default,
    babel = require('gulp-babel'),
    imagemin = require('gulp-imagemin'),
    webp = require('gulp-webp'),
    webpcss = require('gulp-webp-css'),
    svgSprite = require('gulp-svg-sprite'),
    ttf2woff = require('gulp-ttf2woff'),
    ttf2woff2 = require('gulp-ttf2woff2'),
    fonter = require('gulp-fonter'),
    uglify = require('gulp-uglify-es').default,
	livereload = require('gulp-livereload');
    
const css = () => {
    return src(path.src.css)
        // .pipe(wait(1000))
        .pipe(fileinclude())
        .pipe(scss({
            outputStyle: "expanded"
        }))
        .pipe(group_media()) // группирует медиа запросы
        .pipe(autoprefixer({ // добавляет вендорные префиксы
            overrideBrowserslist: ["last 5 versions"],
            cascade: true
        }))
        .pipe(webpcss())
        .pipe(dest(path.build.css))
        .pipe(clean_css())
        .pipe(rename({
            extname: ".min.css"
        }))
        .pipe(dest(path.build.css))
		.pipe(livereload());
}

const js = () => {
    return src(path.src.js)
        .pipe(fileinclude({basepath: '@root'}))
        .pipe(babel({ // изменение кода для старых браузеров
            ignore: [
                "node_modules/**"
            ],
            presets: [
                [
                    "@babel/preset-env",
                    {
                        "modules": false,
                        "targets": {
                            "esmodules": true,
                        },
                    }
                ]
            ],
            sourceMap: false,
            plugins: [
                "@babel/plugin-proposal-class-properties",
            ]
        }))
        .pipe(dest(path.build.js))
        .pipe(uglify())
        .pipe(rename({
            extname: ".min.js"
        }))
        .pipe(dest(path.build.js))
		.pipe(livereload());
}

const images = () => {
    return src(path.src.img)
        .pipe(webp({
            quality: 90,
        }))
        .pipe(dest(path.build.img))
        .pipe(src(path.src.img))
        .pipe(imagemin({
            progressive: true,
            svgoPlugins: [{removeViewBox: false}],
            interlaced: true,
            optimizationLevel: 6 // 0 to 7
        }))
        .pipe(dest(path.build.img))
		.pipe(livereload());
}

// const imagesDjango = () => {
//     return src(path.src.images)
//         .pipe(webp({
//             quality: 90,
//         }))
//         .pipe(dest(path.build.images))
//         .pipe(src(path.src.images))
//         .pipe(imagemin({
//             progressive: true,
//             svgoPlugins: [{removeViewBox: false}],
//             interlaced: true,
//             optimizationLevel: 6 // 0 to 7
//         }))
//         .pipe(dest(path.build.images))
// 		.pipe(livereload());
// }

gulp.task('svgSprite', () => {
    return gulp.src([source_folder + '/iconsprite/*.svg'])
        .pipe(svgSprite({
            mode: {
                stack: {
                    sprite: "../networks/networks.svg", // sprite file name
                    // example: true
                }
            }
        }))
        .pipe(dest(path.build.img))
})

gulp.task('otf2ttf', function() {
    return src([source_folder + '/fonts/*.otf'])
    .pipe(fonter({
      format: ['ttf']
    }))
    .pipe(dest(source_folder + '/fonts/'))
})

const fonts = () => {
    src(path.src.fonts)
        .pipe(ttf2woff())
        .pipe(dest(path.build.fonts))
    return src(path.src.fonts)
        .pipe(ttf2woff2())
        .pipe(dest(path.build.fonts))
}

const watchFiles = () => {
	// livereload.listen();
	gulp.watch([path.watch.css], css);
    gulp.watch([path.watch.js], js);
    gulp.watch([path.watch.img], images);
    // gulp.watch([path.watch.images], imagesDjango);
}

const clean = () => {
    return del(path.clean);
}

let build = gulp.series(clean, gulp.parallel(
	fonts,
	images,
	// imagesDjango,
	js,
	css,
)); // функции кот должны выполняться
let watch = gulp.parallel(build, watchFiles);

// exports.imagesDjango = imagesDjango;
exports.fonts = fonts;
exports.images = images;
exports.js = js;
exports.css = css;
exports.build = build;
exports.watch = watch;
exports.default = watch;
