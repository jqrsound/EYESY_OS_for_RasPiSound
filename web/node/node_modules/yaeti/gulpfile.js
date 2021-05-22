var gulp = require('gulp');
var jscs = require('gulp-jscs');
var jshint = require('gulp-jshint');
var stylish = require('gulp-jscs-stylish');

gulp.task('lint', function()
{
	var src = [ 'gulpfile.js', 'index.js', 'lib/**/*.js' ];

	return gulp.src(src)
		.pipe(jshint('.jshintrc'))
		.pipe(jscs('.jscsrc'))
		.pipe(stylish.combineWithHintResults())
		.pipe(jshint.reporter('jshint-stylish', { verbose: true }))
		.pipe(jshint.reporter('fail'));
});

gulp.task('default', gulp.task('lint'));
