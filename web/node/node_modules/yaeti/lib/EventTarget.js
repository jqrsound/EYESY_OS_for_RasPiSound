function yaetiEventTarget()
{
	this._listeners = {};
}

Object.defineProperties(yaetiEventTarget.prototype,
	{
		listeners:
		{
			get: function()
			{
				return this._listeners;
			}
		}
	});

yaetiEventTarget.prototype.addEventListener = function(type, newListener)
{
	var listenersType;
	var i;
	var listener;

	if (!type || !newListener)
		return;

	listenersType = this._listeners[type];

	if (listenersType === undefined)
		this._listeners[type] = listenersType = [];

	for (i = 0; !!(listener = listenersType[i]); i++)
	{
		if (listener === newListener)
			return;
	}

	listenersType.push(newListener);
};

yaetiEventTarget.prototype.removeEventListener = function(type, oldListener)
{
	var listenersType;
	var i;
	var listener;

	if (!type || !oldListener)
		return;

	listenersType = this._listeners[type];

	if (listenersType === undefined)
		return;

	for (i = 0; !!(listener = listenersType[i]); i++)
	{
		if (listener === oldListener)
		{
			listenersType.splice(i, 1);
			break;
		}
	}

	if (listenersType.length === 0)
		delete this._listeners[type];
};

yaetiEventTarget.prototype.dispatchEvent = function(event)
{
	var type;
	var listenersType;
	var dummyListener;
	var stopImmediatePropagation = false;
	var i;
	var listener;

	if (!event || typeof event.type !== 'string')
		throw new Error('`event` must have a valid `type` property');

	// Do some stuff to emulate DOM Event behavior (just if this is not a
	// DOM Event object).
	if (event._yaeti)
	{
		event.target = this;
		event.cancelable = true;
	}

	// Attempt to override the stopImmediatePropagation() method.
	try
	{
		event.stopImmediatePropagation = function()
		{
			stopImmediatePropagation = true;
		};
	}
	catch (error)
	{}

	type = event.type;
	listenersType = (this._listeners[type] || []);

	dummyListener = this['on' + type];

	if (typeof dummyListener === 'function')
	{
		try
		{
			dummyListener.call(this, event);
		}
		catch (error)
		{
			console.error(error);
		}
	}

	for (i = 0; !!(listener = listenersType[i]); i++)
	{
		if (stopImmediatePropagation)
			break;

		try
		{
			listener.call(this, event);
		}
		catch (error)
		{
			console.error(error);
		}
	}

	return !event.defaultPrevented;
};

module.exports = yaetiEventTarget;
